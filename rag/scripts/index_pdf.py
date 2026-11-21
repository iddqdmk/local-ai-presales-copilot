import argparse
import hashlib
import json
from pathlib import Path

import pymupdf as fitz


def chunk_text(text, size=500, overlap=75):
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("Invalid chunk parameters")

    text = " ".join(text.split())
    step = size - overlap

    for start in range(0, len(text), step):
        chunk = text[start:start + size].strip()
        if chunk:
            yield chunk


def index_pdf(pdf_path, output_path, start_page, end_page):
    pdf_path = Path(pdf_path)
    output_path = Path(output_path)

    if not pdf_path.is_file():
        raise FileNotFoundError(pdf_path)

    sha256 = hashlib.sha256(pdf_path.read_bytes()).hexdigest()

    records = []

    with fitz.open(pdf_path) as document:
        if not (1 <= start_page <= end_page <= len(document)):
            raise ValueError(
                f"Invalid page range. PDF contains {len(document)} pages."
            )

        for page_number in range(start_page, end_page + 1):
            page = document[page_number - 1]
            text = page.get_text("text")

            for chunk_number, chunk in enumerate(chunk_text(text)):
                records.append({
                    "source": pdf_path.name,
                    "page": page_number,
                    "chunk_id": f"p{page_number:04d}-c{chunk_number:03d}",
                    "text": chunk,
                    "vector": [],
                })

    index = {
        "dataset": pdf_path.stem,
        "document_version": "unspecified",
        "source_sha256": sha256,
        "embedding_model": None,
        "chunk_size": 500,
        "chunk_overlap": 75,
        "records": records,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Source:", pdf_path)
    print("Pages:", start_page, "-", end_page)
    print("Chunks:", len(records))
    print("Output:", output_path)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--pdf", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--start-page", type=int, required=True)
    parser.add_argument("--end-page", type=int, required=True)

    args = parser.parse_args()

    index_pdf(
        args.pdf,
        args.output,
        args.start_page,
        args.end_page,
    )


if __name__ == "__main__":
    main()
