"""High-level pipeline orchestration:
- parse PDF
- summarize each element
- embed
- store in Chroma
"""
import os
from .pdf_parser import parse_pdf
from .summarizer import summarize_text, caption_image
from .embedder import embed_texts
from .vectorstore import add_documents


def index_pdf(path_to_pdf: str):
    doc_id, elements = parse_pdf(path_to_pdf)
    texts, metadatas, ids = [], [], []

    for el in elements:
        eid = el.get("id")
        if el.get("type") in ("text", "table"):
            summary = summarize_text(el.get("text", ""))
            texts.append(summary)
            metadatas.append({"doc_id": doc_id, "type": el.get("type"), "page": el.get("page")})
            ids.append(eid)
        elif el.get("type") == "image":
            cap = caption_image(el.get("image_path"))
            texts.append(cap)
            metadatas.append({
                "doc_id": doc_id,
                "type": "image",
                "page": el.get("page"),
                "image_path": el.get("image_path")
            })
            ids.append(eid)

    embeddings = embed_texts(texts)
    add_documents(ids=ids, documents=texts, metadatas=metadatas, embeddings=embeddings)
    print(f"Indexed doc {doc_id} with {len(ids)} items")
    return doc_id
