from crewai import Agent, Task, Crew
from config import llm
from utils import safe_json_parse

def run_agents(topic, slides_num, points_num):
    # Agent 1: Presentation Architect
    architect = Agent(
        role="Presentation Architect",
        goal="Design the structure of a professional presentation based on the topic",
        backstory="Expert in designing and structuring presentations across diverse topics including education, psychology, and social issues.",
        llm=llm,
        verbose=True,
        allow_delegation=True
    )

    structure_task = Task(
        description=f"""
Analyze the topic: "{topic}" and generate a presentation structure with exactly {slides_num} slides.

Slides structure:
1. Title: topic name only.
2. Agenda: list 5–7 main sections that summarize the key content slides. These should group related slides under broader themes.
3. Introduction: brief overview.
4. Main Content slides: each slide should contain:
   - A clear title.
   - {points_num} detailed bullet points (2–3 lines each).
   - Use bullet symbol "•".
5. Fact/Quote/Statistic Slide: include one of:
   - Scientific fact with source.
   - OR famous quote.
   - OR realistic statistic.
6. Conclusion: summarize main insights.
7. “Any Questions?” Slide: contains only "Any Questions?" centered.
8. “Thank You” Slide: contains only "Thank You" centered.

Return the output as a JSON list of slides like this:
[
  {{
    "title": "Slide Title",
    "content": ["• point 1", "• point 2", "• point 3"]
  }}
]
""",
        expected_output="A JSON string representing the slide structure.",
        agent=architect
    )

    # Agent 2: Slide Content Writer
    writer = Agent(
        role="Slide Content Writer",
        goal="Write informative and professional slide content following the given structure and formatting rules",
        backstory="Specialist in writing clear and engaging presentation content for diverse audiences",
        llm=llm,
        verbose=True,
        allow_delegation=True
    )

    content_task = Task(
        description=f"""
Write full slide content for a presentation titled "{topic}" using the provided structure.

Formatting rules:
- Each slide starts with: [Title]
- Use bullet symbol "•"
- Make Introduction a paragraph
- Each bullet point should be 2–3 lines
- Keep tone professional and informative

Structure:
{{structure}}

Return output as JSON list of slides:
[
  {{
    "title": "Slide Title",
    "content": ["• point 1", "• point 2", "• point 3"]
  }}
]
""",
        expected_output="A JSON string representing the full slide content.",
        agent=writer
    )

    # Agent 3: Visual Stylist
    stylist = Agent(
        role="Visual Stylist",
        goal="Choose a suitable visual theme for the presentation including color palette, font style, and mood",
        backstory="Creative designer with experience in presentation aesthetics and audience engagement",
        llm=llm,
        verbose=True,
        allow_delegation=True
    )

    theme_task = Task(
        description=f"""
Choose a suitable visual theme for a presentation titled "{topic}".

Your goal is to select a theme that reflects the scientific and nutritional nature of the topic.

Use:
- Calm, natural colors (e.g., ocean blue, soft gray, white)
- Font style: clean and readable (e.g., Calibri, Segoe UI)
- Mood: scientific, trustworthy, informative

Return output as JSON:
{{
  "color_palette": ["#HEX1", "#HEX2", "#HEX3"],
  "font_style": "Font Name",
  "mood": "Mood description",
  "rationale": "Why it fits the topic"
}}
""",
        expected_output="A JSON string describing the theme.",
        agent=stylist
    )

    # تشغيل الـ Crew لكل Agent
    structure_result = Crew(agents=[architect], tasks=[structure_task]).kickoff()
    structure_json = safe_json_parse(str(structure_result.raw))

    content_result = Crew(agents=[writer], tasks=[content_task]).kickoff(inputs={"structure": structure_json})
    content_json = safe_json_parse(str(content_result.raw))

    theme_result = Crew(agents=[stylist], tasks=[theme_task]).kickoff()
    theme_json = safe_json_parse(str(theme_result.raw))

    return structure_json, content_json, theme_json

