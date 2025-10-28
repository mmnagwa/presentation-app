import streamlit as st
from agents import run_agents
from generator import create_ppt_from_json
from utils import generate_agenda_slide
import random

# Dynamic tips for the robot assistant
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

# Page configuration
st.set_page_config(page_title="🎓 Presentation Generator", layout="centered")

# App title and instructions
st.title("🎓 Presentation Generator")
st.markdown("Talk to the assistant like you're requesting a presentation.")

# Layout: input box + chat.gif
col1, col2 = st.columns([5, 1])
with col1:
    topic = st.text_area("📝 Enter your topic or content")
with col2:
    st.image("assets/chat.gif", width=80)

# Tip section: tip.gif + random tip
with st.container():
    tip_col1, tip_col2 = st.columns([1, 5])
    with tip_col1:
        st.image("assets/tip.gif", width=60)
    with tip_col2:
        st.markdown("💡 *Tip:* " + random.choice(tips))

# Slide settings
slides_num = st.slider("📄 Number of slides", 5, 20, 10)
points_num = st.slider("🔹 Points per slide", 2, 6, 3)

# Generate button
if st.button("Generate Presentation"):
    if not topic.strip():
        st.warning("⚠ Please enter a topic to generate your presentation.")
    else:
        with st.spinner("🤖 Generating your presentation..."):
            # Run the agents to get structure, content, and theme
            structure_json, content_json, theme_json = run_agents(topic, slides_num, points_num)

            # Separate ending slides
            ending_titles = ["conclusion", "any questions?", "thank you"]
            ending_slides = []
            content_slides = []

            for slide in content_json:
                title = slide.get("title", "").strip().lower()
                if title in ending_titles:
                    ending_slides.append(slide)
                else:
                    content_slides.append(slide)

            # Remove agenda if present
            slides_without_agenda = [
                slide for slide in content_slides
                if slide.get("title", "").strip().lower() != "agenda"
            ]

            # Generate agenda slide
            agenda_slide = generate_agenda_slide(slides_without_agenda)

            # Final slide order
            final_slides = [slides_without_agenda[0], agenda_slide] + slides_without_agenda[1:] + ending_slides

            # Create the PowerPoint file
            pptx_path = create_ppt_from_json(final_slides, theme_json, topic)

        # Show success message and success.gif
        st.success("✅ Presentation created!")
        st.image("assets/success.gif", width=300)

        # Download button
        with open(pptx_path, "rb") as f:
            st.download_button("📥 Download Presentation", f, file_name=pptx_path)
