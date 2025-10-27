import os
from dotenv import load_dotenv
from langchain.llms import OpenAI


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ["GOOGLE_API_KEY"] = "AIzaSyDaM9pgt5wef8uXfZt3Wcm8--XxvtB8eRo"
llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
