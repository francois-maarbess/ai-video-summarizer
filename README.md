# 🎬 Multimodal AI Suite: Video Summarization & Secure RAG

A high-performance repository demonstrating the implementation of **Llama-3.2 Vision** and **Vector Search (RAG)** pipelines for automated business intelligence.

## 🚀 Live Demo
* **[Interactive Enterprise RAG Chatbot](https://ai-projects-c409345ucm349us.streamlit.app/)**
* *(Video Summarizer deployment in progress)*

---

## 🛠️ Projects Included

### 1. Universal Video Summarizer (`app.py`)
* **The Tech:** Groq Llama-3.2-11b-vision, MoviePy, Streamlit.
* **The Function:** Processes `.mp4` files by sampling keyframes and analyzing them chronologically to generate intelligent, context-aware summaries.
* **Use Case:** Rapidly extracting action items and insights from meeting recordings and training sessions.

### 2. Secure Enterprise RAG Chatbot (`newapp.py`)
* **The Tech:** FAISS Vector Store, LangChain, Python, Llama-3.3.
* **The Function:** A "Chat with your Data" system using Retrieval-Augmented Generation. It queries local documents (`company_handbook.txt`) while maintaining 100% data privacy.
* **Key Feature:** Engineered to handle sensitive credentials and policy data without external data leaks.

## 📦 Local Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/francois-maarbess/ai-video-summarizer.git](https://github.com/francois-maarbess/ai-video-summarizer.git)
