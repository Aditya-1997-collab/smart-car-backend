# app/routers/ai.py
from fastapi import APIRouter
from app.models.schemas import AIPromptRequest
from app.services.ai_service import hf_client
from app.state import store

router = APIRouter(prefix="/api", tags=["Cloud Intelligence Platform"])

@router.post("/ai-command")
async def bridge_ai_query(payload: AIPromptRequest):
    if not store.feature_flags["enableCloudAI"]:
        return {"reply": "AI Gateway Error: Cloud AI functionality is disabled via Feature Flags."}
        
    if hf_client is None:
        return {"reply": "[Sandbox Mode] HF_TOKEN missing. Processed line: " + payload.prompt}

    try:
        system_instruction = (
            "You are the spatial intelligence engine for a 2-wheel smart robot car. "
            "Answer concisely in one short sentence, focusing on navigation execution rules."
        )
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": payload.prompt}
        ]
        response = hf_client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct:featherless-ai",
            messages=messages,
            max_tokens=60,
            temperature=0.3
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        return {"reply": f"Hugging Face Bridge Pipeline Exception: {str(e)}"}
