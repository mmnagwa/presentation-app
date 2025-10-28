# config.py
import os
from crewai import LLM

google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError("GOOGLE_API_KEY is missing. Please add it to Streamlit Secrets.")

llm = LLM(
    model="gemini/gemini-2.5-flash",  
    api_key=google_api_key,
    temperature=0.7
)

