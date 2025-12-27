import streamlit as st
import requests

# --- PAGE CONFIG ---
st.set_page_config(page_title="Smart Router", page_icon="🧠")

st.title("🧠 The 'Cost-Control' Router")
st.markdown("Type a prompt. The AI will decide if it's **Simple** (Cheap) or **Complex** (Smart).")

# --- SIDEBAR (Stats) ---
st.sidebar.header("💰 Live Savings Tracker")
try:
    # Fetch stats from your backend
    stats_res = requests.get("http://127.0.0.1:8000/stats")
    if stats_res.status_code == 200:
        stats = stats_res.json()
        st.sidebar.metric("Total Money Saved", stats['total_money_saved'])
        st.sidebar.write(f"Total Requests: {stats['total_requests']}")
except:
    st.sidebar.warning("Backend not connected.")

# --- MAIN INTERFACE ---
prompt = st.text_area("Enter your prompt:", height=100)

if st.button("🚀 Run Smart Router"):
    if not prompt:
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Routing..."):
            try:
                # Call YOUR FastAPI Backend
                response = requests.post("http://127.0.0.1:8000/generate", json={"prompt": prompt})
                
                if response.status_code == 200:
                    data = response.json()
                    meta = data['meta']
                    
                    # --- THE "SMART BADGE" DISPLAY ---
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        # Color-coded logic
                        if meta['complexity_assessed'] == "SIMPLE":
                            st.success(f"🌱 {meta['complexity_assessed']}")
                        else:
                            st.error(f"🔥 {meta['complexity_assessed']}")
                            
                    with col2:
                        st.info(f"🤖 {meta['routed_to']}")
                        
                    with col3:
                        st.metric("Savings", meta['money_saved_vs_gpt4'])
                    
                    # --- THE ANSWER ---
                    st.markdown("### Answer")
                    st.write(data['response'])
                    
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("🚨 Connection Error: Is your backend running on Port 8000?")