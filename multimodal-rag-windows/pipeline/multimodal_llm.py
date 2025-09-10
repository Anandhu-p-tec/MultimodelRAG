"""Answer generation using Hugging Face text-generation model."""
import os
from transformers import pipeline
from .summarizer import caption_image

HF_QA_MODEL = os.getenv("HF_QA_MODEL", "google/flan-t5-base")

# Local Hugging Face text-generation pipeline
qa_pipeline = pipeline("text2text-generation", model=HF_QA_MODEL)

PROMPT_TEMPLATE = """
You are an expert assistant. Use the context and image captions below to answer the user question.
Context:
{context}

Image captions:
{image_captions}

Question:
{question}

Answer concisely but with enough detail:
"""

def generate_answer(question: str, contexts: list, images: list):
    context_text = "\n\n".join(contexts)
    image_caps = []
    for p in images:
        try:
            cap = caption_image(p)
        except Exception:
            cap = "[image]"
        image_caps.append(f"- {p}: {cap}")
    image_caps_text = "\n".join(image_caps) if image_caps else "None"

    prompt = PROMPT_TEMPLATE.format(
        context=context_text,
        image_captions=image_caps_text,
        question=question
    )
    out = qa_pipeline(prompt, max_length=300, do_sample=False)
    return out[0]["generated_text"]
