# app/services/ai_service.py
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv() 

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Setup HuggingFace Inference platform referencing Qwen 2.5 Instruct
if GROQ_API_KEY:
    ai_client = Groq(api_key=GROQ_API_KEY)
else:
    ai_client = None
