# ai_core.py
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
# ...
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
# ai_core.py

# ... (imports remain the same)

# --- NEW CONFIGURATION (Updated Dec 2025) ---
ROUTER_MODEL = "llama-3.1-8b-instant"   # Replaces llama3-8b-8192
SMALL_MODEL = "llama-3.1-8b-instant"    # Replaces llama3-8b-8192
LARGE_MODEL = "llama-3.3-70b-versatile" # Replaces llama3-70b-8192 (Newer & Smarter!)

# ... (rest of the file remains the same)

# --- THE ROUTER AGENT ---
def route_prompt(user_prompt: str):
    """
    Uses a small model to classify the prompt complexity.
    Returns: 'SIMPLE' or 'COMPLEX'
    """
    system_instruction = (
        "You are a model router. Analyze the user's prompt. "
        "If it requires simple factual recall, summarization, or chat, output 'SIMPLE'. "
        "If it requires complex reasoning, coding, math, or creative writing, output 'COMPLEX'. "
        "Output ONLY the word 'SIMPLE' or 'COMPLEX'."
    )
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ],
        model=ROUTER_MODEL,
        temperature=0, # Deterministic (we want consistent routing)
        max_tokens=5,  # We only need one word
    )
    
    classification = response.choices[0].message.content.strip().upper()
    # Fallback in case the model yaps
    if "COMPLEX" in classification:
        return "COMPLEX"
    return "SIMPLE"

# --- THE WORKER AGENT ---
def get_response(prompt: str, complexity: str):
    """
    Routes the prompt to the correct model based on complexity.
    """
    if complexity == "COMPLEX":
        model = LARGE_MODEL
        # Simulated savings: GPT-4o costs ~$5/M tokens. Llama-70b (Free) saves that.
        # Let's arbitrary say this query saved $0.01 vs GPT-4
        savings = 0.03 
    else:
        model = SMALL_MODEL
        # Simple queries on GPT-4 are a waste. Saving $0.005
        savings = 0.005

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
    )
    
    return response.choices[0].message.content, model, savings