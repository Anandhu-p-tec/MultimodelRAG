"""Summarizer using Hugging Face Inference API or local transformers."""
import os
from transformers import pipeline
import requests

HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")
HF_SUMMARY_MODEL = os.getenv("HF_SUMMARY_MODEL", "facebook/bart-large-cnn")

# Local pipeline (runs on your machine)
summarizer = pipeline("summarization", model=HF_SUMMARY_MODEL)

def summarize_text(text: str) -> str:
    if not text.strip():
        return ""
    result = summarizer(text, max_length=120, min_length=30, do_sample=False)
    return result[0]["summary_text"]

# Image captioning (still using BLIP if available)
try:
    from transformers import BlipProcessor, BlipForConditionalGeneration
    from PIL import Image

    blip_model_name = os.getenv("MM_IMAGE_CAPTION_MODEL", "Salesforce/blip-image-captioning-base")
    blip_processor = BlipProcessor.from_pretrained(blip_model_name)
    blip_model = BlipForConditionalGeneration.from_pretrained(blip_model_name)
except Exception:
    blip_processor = None
    blip_model = None

def caption_image(image_path: str) -> str:
    if blip_processor and blip_model:
        img = Image.open(image_path).convert("RGB")
        inputs = blip_processor(images=img, return_tensors="pt")
        out_ids = blip_model.generate(**inputs, max_new_tokens=50)
        return blip_processor.decode(out_ids[0], skip_special_tokens=True)
    return "[image]"
