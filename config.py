import os
from crewai import LLM

llm = LLM(
    provider="litellm",
    model="gemini-2.5-flash", 
    temperature=0.7
)


