import streamlit as st
import streamlit.components.v1 as components
from agents import run_agents
from generator import create_ppt_from_json
from utils import generate_agenda_slide
import random

# Dynamic tips
tips = [ ... ]  # نفس القائمة اللي عندك

# Page config
st.set_page_config(page_title="🎓 Presentation Generator", layout="centered")

# Background image from GitHub
st.markdown("""
    <style>
    body {
        background-image: url("https://raw.githubusercontent.com/mnmagwa/presentation-app/main/assets/abstract-technological-background_23-2148897676.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🎓 Presentation Generator")
st.markdown("Talk to the assistant like you're requesting a presentation.")

# Input + robot
col1, col2 = st.columns([5, 1])
with col1:
    topic = st.text_area("📝 Enter your topic or content")
with col2:
    st.image("https://raw.githubusercontent.com/mnmagwa/presentation-app/main/assets/chat.gif", width=120)

# Sliders
slides_num = st.slider("📄 Number of slides", 5, 20, 10)
points_num = st.slider("🔹 Points per slide", 2, 6, 3)

# Generate
if st.button("Generate Presentation"):
    if not topic.strip():
        st.warning("⚠️ Please enter a topic to generate your presentation.")
    else:
        tip_text = random.choice(tips)
        components.html(f"""
        <div id="popup" style="
            position: fixed;
            top: 15%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #fefefe;
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
            <img src="https://raw.githubusercontent.com/mnmagwa/presentation-app/main/assets/tip.gif" width="140" style="margin-bottom: 10px;" />
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

        with st.spinner("🤖 Generating your presentation..."):
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

        st.success("✅ Presentation created!")
        st.image("https://raw.githubusercontent.com/mnmagwa/presentation-app/main/assets/success.gif", width=300)

        with open(pptx_path, "rb") as f:
            st.download_button("📥 Download Presentation", f, file_name=pptx_path)
