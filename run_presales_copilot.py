import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "rag/src"))

from retrieve_multivendor import load_records
from retrieve_multivendor_v2 import retrieve_v2
from answer_multivendor_v1 import validate_citations
from answer_veeam import generate_answer


def run_copilot(question):
    records = load_records()

    retrieval = retrieve_v2(
        question,
        records,
    )

    matches = retrieval["matches"]

    if not matches:
        return {
            "question": question,
            "answer": "В базе знаний не найдено подходящих материалов.",
            "route": retrieval["route"],
            "vendors": retrieval["vendors"],
            "citations": [],
            "invalid_citations": [],
            "evidence": [],
            "status": "NO_EVIDENCE",
        }

    answer = generate_answer(
        question,
        matches,
    )

    citations, invalid = validate_citations(
        answer,
        matches,
    )

    evidence = [
        {
            "vendor": record["vendor"],
            "document_id": record["document_id"],
            "source": record["source"],
            "page": record["page"],
            "chunk_id": record["chunk_id"],
            "score": record["score"],
        }
        for record in matches
    ]

    if invalid:
        status = "INVALID_CITATIONS"
    elif not citations:
        status = "NO_CITATIONS"
    else:
        status = "CITATIONS_STRUCTURALLY_VALID"

    return {
        "question": question,
        "answer": answer,
        "route": retrieval["route"],
        "vendors": retrieval["vendors"],
        "expansion_rules": retrieval["expansion_rules"],
        "citations": [
            {
                "source": source,
                "page": int(page),
                "chunk_id": chunk_id,
            }
            for source, page, chunk_id in citations
        ],
        "invalid_citations": [
            {
                "source": source,
                "page": int(page),
                "chunk_id": chunk_id,
            }
            for source, page, chunk_id in invalid
        ],
        "evidence": evidence,
        "status": status,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Local AI Pre-Sales Copilot MVP"
    )

    parser.add_argument(
        "question",
        help="Question about enterprise infrastructure",
    )

    parser.add_argument(
        "--save",
        action="store_true",
        help="Save result as JSON",
    )

    args = parser.parse_args()

    result = run_copilot(args.question)

    print("\n=== LOCAL AI PRE-SALES COPILOT ===")
    print("Question:", result["question"])
    print("Vendors:", result["vendors"])
    print("Route:", result["route"])

    print("\n=== ANSWER ===\n")
    print(result["answer"])

    print("\n=== CITATION STATUS ===")
    print(result["status"])
    print("Recognized citations:", len(result["citations"]))
    print("Invalid citations:", len(result["invalid_citations"]))

    if args.save:
        output_dir = ROOT / "demo/results"
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now(
            timezone.utc
        ).strftime("%Y%m%d-%H%M%S-%f")

        output_path = (
            output_dir / f"copilot-{timestamp}.json"
        )

        output_path.write_text(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        print("\nSAVED:", output_path)


if __name__ == "__main__":
    main()
