import os
from crewai import LLM
llm = LLM(
    provider="litellm",  
    model="gemini/gemini-2.5-flash", 
    temperature=0.7,
    api_key=os.getenv("GOOGLE_API_KEY") 
)
