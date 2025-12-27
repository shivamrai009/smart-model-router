# 🛡️ Cost-Control LLM Router

A high-performance AI Gateway that intelligently routes prompts to the most cost-effective model without sacrificing quality.

## 🚀 The Problem
Using GPT-4 (or large models) for every simple query (e.g., "Hello") is a waste of money. Using small models for complex math leads to wrong answers.

## 💡 The Solution
This project implements a **Cascading Router Architecture**:
1.  **Incoming Request** hits a FastAPI Endpoint.
2.  **The "Judge" (Llama-3-8B)** analyzes the prompt difficulty in <0.2s.
3.  **Routing Logic:**
    * **Simple Tasks** -> Routed to `Llama-3.1-8B` (Fast/Free).
    * **Complex Tasks** -> Routed to `Llama-3.3-70B` (High Intelligence).
4.  **Analytics:** Logs every decision and calculates simulated savings vs. GPT-4o.

## 🛠️ Tech Stack
* **Backend:** FastAPI (Async Python)
* **AI Engine:** Groq Cloud (Llama 3.1 & 3.3)
* **Database:** SQLite (SQLAlchemy)
* **Frontend:** Streamlit

## 📸 Screenshots

<img width="1763" height="892" alt="Image" src="https://github.com/user-attachments/assets/b35aa7c1-c310-4afa-96d5-70fe4fe8cdf1" />

<img width="1884" height="892" alt="Image" src="https://github.com/user-attachments/assets/c8d54967-a9cf-4c9c-890a-9eb29e014712" />
