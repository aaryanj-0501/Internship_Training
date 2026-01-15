from langchain_community.llms.ollama import Ollama
import os
from dotenv import load_dotenv

load_dotenv()

CHAT_MODEL=os.getenv("CHAT_MODEL_NAME")
llm=Ollama(
    model=CHAT_MODEL,
    temperature=0
)