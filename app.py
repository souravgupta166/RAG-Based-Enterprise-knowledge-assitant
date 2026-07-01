import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from src.loaders import load_document
from src.splitter import chunk_text
from src.vector_store import VectorStore

# -------------------------
# SETUP
# -------------------------
load_dotenv()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="🧠",
    layout="wide"
)

# -------------------------
# VECTOR STORE
# -------------------------
@st.cache_resource
def get_vector_store():
    return VectorStore()

vector_store = get_vector_store()

# -------------------------
# OPENAI CLIENT (OPTIONAL)
# -------------------------
def get_client():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    return OpenAI(api_key=key)

client = get_client()

# -------------------------
# CHAT MEMORY
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:
    st.title("📊 System Status")

    st.metric("Stored Chunks", vector_store.count())

    if client:
        st.success("Reasoning Model: ACTIVE")
    else:
        st.warning("Reasoning Model: LOCAL MODE")

# -------------------------
# DOCUMENT PROCESSING
# -------------------------
def process_files(files):
    total = 0

    for f in files:
        file_path = UPLOAD_DIR / f.name

        with open(file_path, "wb") as file:
            file.write(f.getbuffer())

        text = load_document(file_path)

        if not text:
            continue

        chunks = chunk_text(text)
        stored = vector_store.add_chunks(chunks, f.name)

        total += stored

    return total

# -------------------------
# SMART ANSWER ENGINE
# -------------------------
def generate_answer(question, context, history):

    if not client:
        return f"""
📌 LOCAL MODE RESPONSE

QUESTION:
{question}

CONTEXT:
{context}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are an enterprise AI assistant.

Always respond in this structure:

1. SUMMARY:
- Direct and short answer

2. KEY POINTS:
- Bullet points only from context

3. SOURCE USAGE:
- Mention which context was used

Rules:
- Do not hallucinate
- If not found, say: "Not found in documents"
- Be precise, structured, professional
"""
            },
            {
                "role": "user",
                "content": f"""
CHAT HISTORY:
{history}

DOCUMENT CONTEXT:
{context}

QUESTION:
{question}
"""
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

# -------------------------
# UI
# -------------------------
st.title("🧠 Enterprise Knowledge Assistant")
st.caption("RAG + Memory + Smart AI Reasoning")

# -------------------------
# UPLOAD SECTION
# -------------------------
st.subheader("📄 Upload Documents")

files = st.file_uploader(
    "Upload PDF, DOCX, TXT files",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

if st.button("Process Documents"):
    if not files:
        st.warning("Please upload files first")
    else:
        with st.spinner("Processing documents..."):
            total = process_files(files)

        st.success(f"Chunks stored: {total}")

# -------------------------
# CHAT HISTORY
# -------------------------
st.divider()
st.subheader("💬 Chat with your documents")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# USER INPUT
# -------------------------
user_input = st.chat_input("Ask something about your documents...")

if user_input:

    # save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # -------------------------
    # RETRIEVAL
    # -------------------------
    results = vector_store.search(user_input, top_k=8)

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    # -------------------------
    # SMART FILTERING
    # -------------------------
    filtered_docs = []
    filtered_metas = []

    for doc, meta, dist in zip(docs, metas, distances):

        if dist is None:
            continue

        if dist < 1.2:
            filtered_docs.append(doc)
            filtered_metas.append(meta)

    if not filtered_docs:
        filtered_docs = docs[:3]
        filtered_metas = metas[:3]

    # -------------------------
    # CONTEXT BUILDING
    # -------------------------
    context = "\n\n".join(
        f"[Source: {m.get('source','unknown')}]\n{d}"
        for d, m in zip(filtered_docs, filtered_metas)
    )

    # -------------------------
    # CHAT HISTORY BUILD
    # -------------------------
    history = ""
    for m in st.session_state.messages[-6:]:
        role = "User" if m["role"] == "user" else "Assistant"
        history += f"{role}: {m['content']}\n"

    # -------------------------
    # GENERATE ANSWER
    # -------------------------
    answer = generate_answer(user_input, context, history)

    # save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.markdown("### 🧠 Answer")
        st.markdown(answer)