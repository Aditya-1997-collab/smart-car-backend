# app/services/ai_service.py
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv() 

HF_TOKEN = os.environ.get("HF_TOKEN")

print(HF_TOKEN)

# Setup HuggingFace Inference platform referencing Qwen 2.5 Instruct
if HF_TOKEN:
    hf_client = InferenceClient(
        api_key=os.environ["HF_TOKEN"],
    )
else:
    hf_client = None
