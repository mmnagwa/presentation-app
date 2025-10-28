import streamlit as st
import streamlit.components.v1 as components
from agents import run_agents
from generator import create_ppt_from_json
from utils import generate_agenda_slide
import random

# Tips
tips = [
    "🎤 Don’t read your slides — your audience can read faster than you!",
    "🧙 Pretend your laser pointer is a lightsaber — but use it wisely.",
    "🔤 One font to rule them all. Please, no Comic Sans 😅.",
    "🚀 Your first slide is your first impression — make it pop, not flop!",
    "⏰ If you run out of time, smile confidently — they’ll think it was planned 😉.",
    "📚 Avoid putting whole essays on slides — it’s a presentation, not a novel!",
    "🎬 Practice like you’re on Netflix — aim to entertain, not just inform.",
    "😴 If your audience yawns, ask a question. If they still yawn, ask a weird one!",
    "🖼 A picture is worth a thousand bullet points.",
    "🙈 Don’t apologize for your slides — they can’t hear you anyway.",
    "💫 Animations are cool... until they’re not. Keep it classy!",
    "🖲 Always test your clicker — it’s your best friend on stage.",
    "💧 Keep water nearby. Presenting without it is like running a marathon in the desert.",
    "🎙 Your mic doesn’t make you Beyoncé — speak clearly, not loudly!",
    "🧂 Use transitions like salt — a pinch adds flavor, too much ruins everything.",
    "👀 Never say 'Can you all see this?' — they can, and now they’re distracted.",
    "📖 If your slide has more text than a Wikipedia page... start over.",
    "😊 Smile — it’s free design for your face!",
    "🤓 If your joke flops, just say 'That one’s for the data scientists.'",
    "🧩 Don’t argue with your slides — they always win.",
    "👁 Make eye contact with humans, not the screen.",
    "⏸ Pause — it makes you sound smart and dramatic.",
    "🤖 If something breaks, make it part of the show — own the chaos!",
    "💪 Confidence beats perfection. Every. Single. Time.",
    "📱 End before they start checking their phones 😬."
]

# Page config
st.set_page_config(page_title="🎓 Presentation Generator", layout="centered")

# Background image from GitHub
st.markdown("""
    <style>
    body {
        background-image: url("assets/abstract-technological-background_23-2148897676.jpg?raw=true");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📃 Presentation Generator")
st.markdown("Talk to the assistant like you're requesting a presentation.")

# Input + chat.gif
col1, col2 = st.columns([5, 1])
with col1:
    topic = st.text_area("📝 Enter your topic or content")
with col2:
    st.image("assets/chat.gif", width=120)

# Sliders
slides_num = st.slider("📄 Number of slides", 5, 20, 10)
points_num = st.slider("🔹 Points per slide", 2, 6, 3)

# Generate presentation button
if st.button("Generate Presentation"):
    if not topic.strip():
        st.warning("⚠️ Please enter a topic to generate your presentation.")
    else:
        # Show a random tip popup
        tip_text = random.choice(tips)
        components.html(f"""
        <div id="popup" style="
            position: fixed;
            top: 4%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(255, 255, 255, 0.8);
            border: 2px solid #ccc;
            border-radius: 16px;
            padding: 20px;
            z-index: 9999;
            box-shadow: 0 0 30px rgba(0,0,0,0.3);
            width: 420px;
            text-align: center;
            font-family: 'Segoe UI', sans-serif;
            animation: fadeIn 0.6s ease-in-out;
        ">
            <img src="assets/tip.gif?raw=true" width="100" style="margin-bottom: 10px;" />
            <h4 style="margin-bottom: 10px;">💡 Presentation Tip</h4>
            <p style="font-size: 16px;">{tip_text}</p>
            <button onclick="document.getElementById('popup').style.display='none'" style="
                margin-top: 12px;
                padding: 8px 16px;
                background-color: #ff4b4b;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
            ">Close</button>
        </div>

        <style>
        @keyframes fadeIn {{
          from {{ opacity: 0; transform: scale(0.9); }}
          to {{ opacity: 1; transform: scale(1); }}
        }}
        </style>
        """, height=350)

        # Show loading message under the button
        loading_msg = st.empty()
        loading_msg.markdown("### 🧠 Generating your presentation...")

        with st.spinner("Please wait..."):
            structure_json, content_json, theme_json = run_agents(topic, slides_num, points_num)

            ending_titles = ["conclusion", "any questions?", "thank you"]
            ending_slides = []
            content_slides = []

            for slide in content_json:
                title = slide.get("title", "").strip().lower()
                if title in ending_titles:
                    ending_slides.append(slide)
                else:
                    content_slides.append(slide)

            slides_without_agenda = [
                slide for slide in content_slides
                if slide.get("title", "").strip().lower() != "agenda"
            ]

            agenda_slide = generate_agenda_slide(slides_without_agenda)
            final_slides = [slides_without_agenda[0], agenda_slide] + slides_without_agenda[1:] + ending_slides

            pptx_path = create_ppt_from_json(final_slides, theme_json, topic)

        loading_msg.empty()

        st.success("✅ Presentation created!")
        st.image("assets/success.gif", width=120)

        with open(pptx_path, "rb") as f:
            st.download_button("📥 Download Presentation", f, file_name=pptx_path)
