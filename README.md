# 🎬 AI Video Summarizer & Secure RAG Chatbot

This repository contains two high-performance AI pipelines built with **Python**, **Groq (Llama 3.2 Vision)**, and **LangChain**.

## 🚀 Projects Included

### 1. Universal Video Summarizer
* **Tech:** Groq Llama-3.2-11b-vision, Streamlit, MoviePy.
* **Function:** Upload any `.mp4`, and the AI samples frames to provide a chronological, intelligent summary.
* **Status:** ⚡ Live API Key included in `Meeting-summarizer.py` for public testing.

### 2. Secure Local RAG Chatbot
* **Tech:** LangChain, FAISS/ChromaDB, Python.
* **Function:** Chat with local documents (`company_handbook.txt`) with 100% data privacy.
* **Security Test:** Successfully retrieved the "Swordfish" password from encrypted-style local text files.

## 📦 Quick Start
1. **Clone the repo:**
   `git clone https://github.com/francois-maarbess/ai-video-summarizer.git`
2. **Install dependencies:**
   `pip install streamlit groq moviepy langchain`
3. **Run the Video Summarizer:**
   `streamlit run app.py`
