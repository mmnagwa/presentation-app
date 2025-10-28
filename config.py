import os
from crewai.llm import LLM 
from litellm import completion
llm = LLM(
    provider="litellm",  
    model="gemini/gemini-2.5-flash", 
    temperature=0.7,
    api_key=os.getenv("GOOGLE_API_KEY") 
)
