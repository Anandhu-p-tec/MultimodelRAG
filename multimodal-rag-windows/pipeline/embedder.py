"""Embeds text using sentence-transformers (local) by default.
If you prefer OpenAI embeddings, you can switch to OpenAIEmbeddings from langchain.
"""
import os
from sentence_transformers import SentenceTransformer

MODEL_NAME = os.getenv("HF_EMBEDDING_MODEL", "all-MiniLM-L6-v2")

print("Loading embedding model:", MODEL_NAME)
embed_model = SentenceTransformer(MODEL_NAME)


def embed_texts(texts: list):
    embs = embed_model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    return embs.tolist()


def embed_text(text: str):
    return embed_texts([text])[0]
