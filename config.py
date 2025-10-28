import os
import google.generativeai as genai
from crewai import LLM
google_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)


llm = LLM(
     provider="gemini",
    model="gemini-1.5-flash",  
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)






