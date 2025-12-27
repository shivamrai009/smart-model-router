# main.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, RequestLog
import ai_core

app = FastAPI(title="Cost-Control Router")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate_response(request: UserRequest, db: Session = Depends(get_db)):
    # 1. ROUTING STEP
    # The router analyzes the prompt.
    complexity = ai_core.route_prompt(request.prompt)
    
    # 2. GENERATION STEP
    # The appropriate model (Worker) generates the text.
    response_text, model_used, savings = ai_core.get_response(request.prompt, complexity)
    
    # 3. LOGGING STEP (Data Infra)
    # We record what happened for analytics.
    log_entry = RequestLog(
        prompt=request.prompt,
        complexity=complexity,
        model_used=model_used,
        estimated_cost_saved=savings
    )
    db.add(log_entry)
    db.commit()
    
    return {
        "response": response_text,
        "meta": {
            "complexity_assessed": complexity,
            "routed_to": model_used,
            "money_saved_vs_gpt4": f"${savings}"
        }
    }

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """View how much money we've saved!"""
    total_savings = db.query(RequestLog).with_entities(RequestLog.estimated_cost_saved).all()
    total = sum([x[0] for x in total_savings])
    return {"total_money_saved": f"${total:.2f}", "total_requests": len(total_savings)}