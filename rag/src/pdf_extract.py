
import argparse
import json
from pathlib import Path

import pymupdf


def extract_pdf(pdf_path, output_path, start_page, max_pages):
    results = []

    with pymupdf.open(pdf_path) as doc:
        total_pages = len(doc)

        if start_page < 1 or start_page > total_pages:
            raise ValueError("Invalid starting page")

        end_page = min(start_page - 1 + max_pages, total_pages)

        print(f"Total PDF pages: {total_pages}")
        print(f"Processing pages: {start_page}–{end_page}")

        for page_index in range(start_page - 1, end_page):
            page = doc[page_index]
            text = page.get_text("text", sort=True).strip()

            results.append({
                "source": pdf_path.name,
                "page": page_index + 1,
                "text": text
            })

            print(
                f"Page {page_index + 1}: "
                f"{len(text)} characters"
            )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("pdf", type=Path)
    parser.add_argument("--start-page", type=int, default=1)
    parser.add_argument("--pages", type=int, default=5)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("rag/index/veeam-pages.json")
    )

    args = parser.parse_args()

    if args.pages < 1 or args.pages > 20:
        parser.error("--pages must be between 1 and 20")

    extract_pdf(
        args.pdf,
        args.output,
        args.start_page,
        args.pages
    )

