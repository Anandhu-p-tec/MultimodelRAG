"""High-level retrieval: embed the query and return matched doc metadata + text.
"""
from .embedder import embed_text
from .vectorstore import query_embeddings


def retrieve(query: str, k=5):
    q_emb = embed_text(query)
    res = query_embeddings(q_emb, n_results=k)
    hits = []
    for idx, doc_text in enumerate(res.get("documents", [[]])[0]):
        meta = res.get("metadatas", [[]])[0][idx]
        hit_id = res.get("ids", [[]])[0][idx]
        hits.append({"id": hit_id, "text": doc_text, "metadata": meta})
    return hits
