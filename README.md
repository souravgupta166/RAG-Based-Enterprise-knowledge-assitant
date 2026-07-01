# 🧠 Enterprise Knowledge Assistant (RAG-based AI System)

A production-style **Retrieval-Augmented Generation (RAG) AI assistant** that allows users to upload enterprise documents and ask intelligent questions in natural language. The system retrieves relevant context from documents and generates accurate, context-aware responses using AI.

🌐 **Live Demo:**  
https://fuqnxiytmb7kudvn6cvdps.streamlit.app/

---

## 📌 Key Features

- 📄 Upload PDF, DOCX, and TXT documents
- 🧩 Automatic text chunking for efficient retrieval
- 🧠 Vector-based semantic search using ChromaDB
- 🔍 Context-aware document retrieval
- 💬 Chat-style interface with memory support
- 🤖 AI-powered answer generation (OpenAI GPT integration)
- 🧱 Local fallback mode (works even without API)
- ⚡ Fast, lightweight Streamlit UI

---

## 🏗️ Architecture

User Query
↓
Streamlit UI (app.py)
↓
Vector Search (ChromaDB)
↓
Semantic Embeddings (SentenceTransformers)
↓
Relevant Context Retrieval
↓
LLM (OpenAI GPT-4o-mini)
↓
Final Answer to User


---

## ⚙️ Tech Stack

- **Frontend:** Streamlit
- **LLM:** OpenAI GPT (optional)
- **Embeddings:** SentenceTransformers (all-MiniLM-L6-v2)
- **Vector Database:** ChromaDB
- **Document Processing:** PyMuPDF, python-docx
- **Language:** Python

---

## 📁 Project Structure

```

RAG-Based-Enterprise-Knowledge-Assistant/
│
├── app.py                  # Main Streamlit application
├── requirements.txt       # Dependencies
├── src/
│   ├── loaders.py         # Document loaders (PDF/DOCX/TXT)
│   ├── splitter.py        # Text chunking logic
│   ├── vector\_store.py    # Embeddings + vector DB logic
│
├── data/
│   └── uploads/           # Uploaded files (local only)
│
├── chroma\_db/             # Vector database storage
└── .streamlit/            # Streamlit configuration

🚀 How It Works
Upload Documents
User uploads enterprise documents (PDF/DOCX/TXT)
Text Processing
Documents are parsed and split into meaningful chunks
Embedding Generation
Each chunk is converted into vector embeddings
Vector Storage
Embeddings are stored in ChromaDB for fast retrieval
Query Handling
User question is embedded and matched with relevant chunks
Answer Generation
Retrieved context is passed to LLM for final response
🧠 Why This Project Matters

This project demonstrates:

Real-world RAG pipeline implementation
End-to-end AI system design
Practical LLM integration
Vector database usage in production workflows
Chat-style AI application development
Deployment-ready AI engineering skills
🔥 Example Use Cases
Internal company knowledge base assistant
HR policy Q&A bot
Document summarization system
Enterprise search engine
Customer support automation assistant
📦 Installation (Local Setup)
git clone https://github.com/your-username/your-repo.git
cd RAG-Based-Enterprise-Knowledge-Assistant

pip install -r requirements.txt

streamlit run app.py
🔐 Environment Variables

Create a .env file:

OPENAI_API_KEY=your_api_key_here
📈 Future Improvements
Citation-based responses (source highlighting)
Streaming response UI (ChatGPT-style typing)
Multi-document comparison mode
Authentication layer for enterprise use
API backend using FastAPI
👨‍💻 Author

Sourav Gupta

AI/ML Developer | Building Production-Grade AI Systems
