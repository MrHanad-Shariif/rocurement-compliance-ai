from fastapi import APIRouter
from pydantic import BaseModel
from app.ai_chatbot_knowledge import knowledge_base

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    user_question = request.question.lower()
    best_match = None
    for entry in knowledge_base:
        if any(keyword in user_question for keyword in entry["keywords"]):
            best_match = entry["answer"]
            break
    if not best_match:
        # Use the fallback (last) entry
        best_match = knowledge_base[-1]["answer"]
    return ChatResponse(answer=best_match) 