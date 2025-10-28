import re
import json
from pptx.dml.color import RGBColor

def hex_to_rgb(hex_color):
    return RGBColor(
        int(hex_color[1:3], 16),
        int(hex_color[3:5], 16),
        int(hex_color[5:7], 16)
    )

def is_dark_color(hex_color):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    return brightness < 128

def shorten_paragraph(text, max_sentences=2):
    sentences = re.split(r'(?<=[.!?]) +', text)
    return ' '.join(sentences[:max_sentences])

def slugify(text):
    return re.sub(r'\W+', '_', text.strip().lower())

def safe_json_parse(raw_text):
    try:
        cleaned = re.search(r'\[.*\]|\{.*\}', raw_text, re.DOTALL)
        if cleaned:
            return json.loads(cleaned.group(0))
        print("⚠️ No valid JSON found in:", raw_text[:200])
        return []
    except json.JSONDecodeError as e:
        print("❌ JSON parsing error:", e)
        print("Raw text snippet:", raw_text[:300])
        return []

def generate_agenda_slide(slides):
    main_titles = []
    for slide in slides:
        title = slide.get("title", "").strip()
        if not title:
            continue
        title_lower = title.lower()
        if any(x in title_lower for x in ["introduction", "conclusion", "thank", "question"]):
            continue
        main_titles.append(title)

    main_ideas = main_titles[:4]

    return {
        "title": "Agenda",
        "content": [
            "• Introduction",
            "• " + "\n• ".join(main_ideas),
            "• Conclusion"
        ]
    }





