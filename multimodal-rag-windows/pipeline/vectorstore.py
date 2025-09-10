"""Chroma vectorstore wrapper using new chromadb client API.
Stores docs with ids/metadatas/embeddings.
"""
import os
import chromadb

PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma_db")

# New style client
client = chromadb.PersistentClient(path=PERSIST_DIR)

COLLECTION_NAME = "multimodal_docs"


def get_collection():
    try:
        return client.get_collection(COLLECTION_NAME)
    except Exception:
        return client.create_collection(name=COLLECTION_NAME)


def add_documents(ids, documents, metadatas, embeddings):
    col = get_collection()
    col.add(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)


def query_embeddings(query_embedding, n_results=5):
    col = get_collection()
    result = col.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["metadatas", "documents"],
    )
    return result
