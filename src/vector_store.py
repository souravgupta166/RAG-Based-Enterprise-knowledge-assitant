import hashlib
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_PATH = Path("chroma_db")


class VectorStore:
    def __init__(self):
        CHROMA_PATH.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        self.collection = self.client.get_or_create_collection("enterprise_docs")

        # local embedding model (NO API)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, texts):
        return self.model.encode(texts).tolist()

    def make_id(self, source, i, text):
        return hashlib.md5(f"{source}_{i}_{text[:100]}".encode()).hexdigest()

    def add_chunks(self, chunks, source_name):
        chunks = [c.strip() for c in chunks if c and c.strip()]
        if not chunks:
            return 0

        embeddings = self.embed(chunks)

        ids = [self.make_id(source_name, i, c) for i, c in enumerate(chunks)]

        metadatas = [
            {"source": source_name, "chunk_id": i}
            for i in range(len(chunks))
        ]

        self.collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

        return len(chunks)

    def search(self, query, top_k=5):
        if self.collection.count() == 0:
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

        q_emb = self.embed([query])[0]

        return self.collection.query(
            query_embeddings=[q_emb],
            n_results=top_k
        )

    def count(self):
        return self.collection.count()