import requests
import time

# Since we are inside the Codespace, we can talk to localhost directly.
API_URL = "http://127.0.0.1:8000/generate"

# A mix of easy and hard prompts to test the router's decision making
prompts = [
    "What is the capital of France?",                                    # SIMPLE
    "Write a Python script to merge two sorted lists.",                  # COMPLEX
    "Who is the CEO of Tesla?",                                          # SIMPLE
    "Explain the difference between TCP and UDP in networking.",         # COMPLEX
    "What is 10 + 10?",                                                  # SIMPLE
    "Design a SQL schema for a library management system.",              # COMPLEX
]

print(f"🚀 Starting Stress Test on {API_URL}...\n")

for i, p in enumerate(prompts):
    start = time.time()
    try:
        response = requests.post(API_URL, json={"prompt": p})
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract data
            complexity = data['meta']['complexity_assessed']
            model = data['meta']['routed_to']
            savings = data['meta']['money_saved_vs_gpt4']
            
            # Print cleanly
            print(f"[{i+1}] Prompt: {p[:40]}...")
            print(f"    👉 Router Said:   {complexity}")
            print(f"    🤖 Model Used:    {model}")
            print(f"    💰 Savings:       {savings}")
            print("-" * 50)
        else:
            print(f"❌ Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"❌ Connection Error: {e}")
        print("Make sure your uvicorn server is running in another terminal!")