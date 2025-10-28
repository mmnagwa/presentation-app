import os
from crewai import LLM
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
llm = LLM(
    model="gemini/gemini-2.5-flash", 
    temperature=0.7,

)
