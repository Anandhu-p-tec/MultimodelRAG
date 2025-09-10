"""PDF parsing: pdfplumber + fitz fallback, with optional `unstructured` use if available.
This extracts text blocks, table text (as CSV/html), and images into a per-doc folder.
"""
import os
import uuid
import pdfplumber
import fitz  # pymupdf
from pathlib import Path


def ensure_dir(p):
    Path(p).mkdir(parents=True, exist_ok=True)


def extract_with_pdfplumber(pdf_path, out_dir):
    ensure_dir(out_dir)
    docs = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                docs.append({
                    "id": str(uuid.uuid4()),
                    "type": "text",
                    "page": i,
                    "text": text,
                })
            tables = page.extract_tables()
            for t in tables:
                csv = "\n".join([",".join([str(cell or "") for cell in row]) for row in t])
                docs.append({
                    "id": str(uuid.uuid4()),
                    "type": "table",
                    "page": i,
                    "text": csv,
                })
    return docs


def extract_images_with_fitz(pdf_path, out_dir):
    ensure_dir(out_dir)
    images = []
    doc = fitz.open(pdf_path)
    for page_index in range(len(doc)):
        for img_index, img in enumerate(doc.get_page_images(page_index)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image.get("ext", "png")
            img_name = f"image_p{page_index+1}_{img_index}.{ext}"
            img_path = os.path.join(out_dir, img_name)
            with open(img_path, "wb") as f:
                f.write(image_bytes)
            images.append({
                "id": str(uuid.uuid4()),
                "type": "image",
                "page": page_index + 1,
                "image_path": img_path,
            })
    return images


def parse_pdf(pdf_path, out_root="./data/docs"):
    pdf_path = str(pdf_path)
    doc_id = Path(pdf_path).stem + "_" + str(uuid.uuid4())[:8]
    out_dir = os.path.join(out_root, doc_id)
    ensure_dir(out_dir)
    try:
        from unstructured.partition.pdf import partition_pdf
        elements = partition_pdf(
            filename=pdf_path,
            strategy="hi_res",
            pdf_infer_table_structure=True,
            extract_images_in_pdf=True
        )
        parsed = []
        for el in elements:
            el_type = getattr(el, "type", None) or getattr(el, "element_type", None) or "text"
            if el_type and "Text" in str(el_type):
                parsed.append({
                    "id": str(uuid.uuid4()),
                    "type": "text",
                    "page": getattr(el, "page_number", None),
                    "text": getattr(el, "text", "")
                })
            elif el_type and ("Table" in str(el_type) or "TableRow" in str(el_type)):
                parsed.append({
                    "id": str(uuid.uuid4()),
                    "type": "table",
                    "page": getattr(el, "page_number", None),
                    "text": getattr(el, "text", "")
                })
            else:
                img_path = getattr(el, "filename", None)
                if img_path:
                    parsed.append({
                        "id": str(uuid.uuid4()),
                        "type": "image",
                        "page": getattr(el, "page_number", None),
                        "image_path": img_path,
                    })
        imgs = extract_images_with_fitz(pdf_path, out_dir)
        parsed.extend(imgs)
        return doc_id, parsed
    except Exception as e:
        print("unstructured not available or failed; falling back:", e)
        texts = extract_with_pdfplumber(pdf_path, out_dir)
        imgs = extract_images_with_fitz(pdf_path, out_dir)
        parsed = texts + imgs
        return doc_id, parsed
