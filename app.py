import streamlit as st
import requests

API_URL = "http://localhost:8000/api/v1"

st.set_page_config(page_title="Uncertainty-Aware RAG", page_icon="🧠", layout="wide")
st.title("🧠 Uncertainty-Aware RAG System")

# --- SIDEBAR: Document Upload ---
with st.sidebar:
    st.header("📄 Knowledge Base")
    st.write("Upload PDFs to add them to the vector database.")
    
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    if st.button("Upload & Process") and uploaded_file:
        with st.spinner("Uploading to FastAPI and queuing task..."):
            # Send file to FastAPI
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            resp = requests.post(f"{API_URL}/documents/", files=files)
            
            if resp.status_code == 201:
                st.success(f"✅ Uploaded! Celery worker is processing it.")
            elif resp.status_code == 400:
                st.warning("⚠️ This document was already uploaded.")
            else:
                st.error("❌ Upload failed.")

# --- MAIN CHAT INTERFACE ---
# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input field
if prompt := st.chat_input("Ask a question about your documents..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI to get answer
    with st.chat_message("assistant"):
        with st.spinner("Searching vectors and calculating LLM uncertainty..."):
            try:
                # 1. Fetch the raw search context first to display to the user
                search_resp = requests.get(f"{API_URL}/search/", params={"query": prompt})
                retrieved_chunks = search_resp.json().get("results", [])
                
                # 2. Fetch the LLM answer
                resp = requests.get(f"{API_URL}/search/ask", params={"query": prompt})
                
                if resp.status_code == 200:
                    data = resp.json()
                    answer = data["answer"]
                    confidence = data.get("generation_confidence")
                    is_uncertain = data.get("is_uncertain", False)
                    
                    # Safely format the confidence score if it exists
                    conf_display = f"{confidence:.2f}" if confidence is not None else "N/A"
                    
                    # Display mathematical confidence
                    if is_uncertain:
                        st.warning(f"⚠️ **High Uncertainty Flagged** (Confidence: {conf_display}). The system does not have enough context to answer safely.")
                    else:
                        st.caption(f"Mathematical Confidence: {conf_display}")
                        
                    st.markdown(answer)
                    
                    # NEW: Display the retrieved context chunks in a dropdown
                    with st.expander("🔍 View Retrieved Context (Debug)"):
                        if retrieved_chunks:
                            for i, chunk in enumerate(retrieved_chunks):
                                st.markdown(f"**Chunk {i+1} (Score: {chunk['score']:.2f}):**\n\n_{chunk['text']}_")
                        else:
                            st.write("No context retrieved from database.")
                            
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"API Error: {resp.text}")
            except Exception as e:
                st.error(f"Failed to connect to API. Is Uvicorn running? Error: {e}")