import sys
from pathlib import Path
from pipeline.pipeline import index_pdf

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scripts/index_pdf.py path/to/file.pdf")
        sys.exit(1)
    pdf = sys.argv[1]
    if not Path(pdf).exists():
        print("File not found:", pdf)
        sys.exit(1)
    index_pdf(pdf)
