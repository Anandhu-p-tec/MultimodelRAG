import streamlit as st
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from scripts.index_pdf import index_pdf
from pipeline.retriever import retrieve
from pipeline.multimodal_llm import generate_answer
from pathlib import Path

st.set_page_config(page_title="Multimodal RAG — Demo")
st.title("Multimodal RAG — PDF Q&A  ")

uploaded = st.file_uploader("Upload a PDF", type=["pdf"])
if uploaded:
    save_path = Path("./data/docs") / uploaded.name
    with open(save_path, "wb") as f:
        f.write(uploaded.getbuffer())
    st.success("Saved PDF to data/docs. Indexing...")
    doc_id = index_pdf(str(save_path))
    st.success(f"Indexed: {doc_id}")

query = st.text_input("Ask a question about uploaded docs")
if st.button("Search") and query:
    hits = retrieve(query, k=5)
    contexts = [h['text'] + f"\n(source: {h['metadata'].get('doc_id')})" for h in hits]
    images = [h['metadata'].get('image_path') for h in hits if h['metadata'].get('image_path')]
    answer = generate_answer(query, contexts, images)
    st.markdown("**Answer:**")
    st.write(answer)
    st.markdown("**Sources:**")
    for h in hits:
        st.write(h['metadata'])
