import streamlit as st
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq

# --- 1. SET UP THE PAGE ---
st.set_page_config(page_title="Private AI Vault", page_icon="🔒")
st.title("🔒 My Private Company AI")
st.markdown("Ask anything about the handbook. I only answer using your local data.")

# --- 2. LOAD BRAIN (Cached so it's fast) ---
import os
from pathlib import Path

# --- 2. LOAD BRAIN (Auto-updates if file changes) ---
def get_file_mtime(filepath):
    return os.path.getmtime(filepath)

# We add the file's modification time as a parameter. 
# If the time changes, the cache resets!
@st.cache_resource
def load_resources(mtime):
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    # --- SMART READ LOGIC ---
    try:
        # Try standard UTF-8 first (GitHub's default)
        with open("company_handbook.txt", "r", encoding="utf-8") as f:
            text = f.read()
    except UnicodeDecodeError:
        # Fallback to UTF-16 if it's a Windows-style file
        with open("company_handbook.txt", "r", encoding="utf-16") as f:
            text = f.read()
    
    # Chunking
    chunks = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    # Build the FAISS index
    embeddings = embedder.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings).astype('float32'))
    
    return embedder, index, chunks

# This line checks the file time and triggers the update
current_mtime = get_file_mtime("company_handbook.txt")
embedder, index, chunks = load_resources(current_mtime)

# --- 3. THE SIDEBAR (Settings) ---
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Groq API Key", type="password")
    st.info("This app searches your local 'company_vault.index' file.")

# --- 4. THE CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- THE RAG LOGIC ---
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar!")
    else:
        with st.spinner("Searching vault..."):
            # Search
            query_emb = embedder.encode([prompt]).astype('float32')
            D, I = index.search(query_emb, k=1)
            context = chunks[I[0][0]]

            # Generate
            client = Groq(api_key=api_key)
            full_prompt = f"Context: {context}\n\nQuestion: {prompt}"
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": full_prompt}]
            )
            answer = response.choices[0].message.content

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
