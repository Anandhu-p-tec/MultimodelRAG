from pipeline.retriever import retrieve
from pipeline.multimodal_llm import generate_answer

if __name__ == '__main__':
    q = input("Question: ")
    hits = retrieve(q, k=5)
    contexts = [h['text'] + f"\n(source: {h['metadata'].get('doc_id')})" for h in hits]
    images = [h['metadata'].get('image_path') for h in hits if h['metadata'].get('image_path')]
    ans = generate_answer(q, contexts, images)
    print('\n=== ANSWER ===\n')
    print(ans)
