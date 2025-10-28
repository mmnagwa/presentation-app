import os
from crewai import LLM
llm = LLM(
    model="gemini/gemini-2.5-flash",
    temperature=0.7
)
