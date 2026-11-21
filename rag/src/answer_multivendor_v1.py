import re
import sys

from retrieve_multivendor import load_records
from retrieve_multivendor_v2 import retrieve_v2
from answer_veeam import generate_answer


def validate_citations(answer, matches):
    allowed = {
        (
            str(record["source"]),
            str(record["page"]),
            str(record["chunk_id"]),
        )
        for record in matches
    }

    pattern = re.compile(
        r"\[([^,\[\]]+),\s*page\s+(\d+),\s*chunk\s+([^\[\],\s]+)\]"
    )

    citations = pattern.findall(answer)

    invalid = [
        citation
        for citation in citations
        if citation not in allowed
    ]

    return citations, invalid


def main():
    if len(sys.argv) < 2:
        print(
            'Usage: python rag/src/answer_multivendor_v1.py "question"'
        )
        sys.exit(1)

    question = " ".join(sys.argv[1:])

    records = load_records()
    result = retrieve_v2(question, records)
    matches = result["matches"]

    print("=== MULTI-VENDOR RAG V1 ===")
    print("Question:", question)
    print("Vendors:", result["vendors"])
    print("Expansion:", result["expansion_rules"])
    print("Retrieved chunks:", len(matches))

    if not matches:
        print("No evidence found.")
        return

    print("\n=== EVIDENCE ===")

    for record in matches:
        print(
            f"{record['vendor']} | "
            f"page={record['page']} | "
            f"chunk={record['chunk_id']}"
        )

    print("\n=== ANSWER ===")

    answer = generate_answer(question, matches)
    print(answer)

    citations, invalid = validate_citations(answer, matches)

    print("\n=== CITATION CHECK ===")
    print("Recognized citations:", len(citations))
    print("Invalid citations:", len(invalid))

    for citation in invalid:
        print("INVALID:", citation)

    if not citations:
        print("WARNING: No recognized citations found.")

    if invalid:
        print("WARNING: Answer contains unsupported citation references.")


if __name__ == "__main__":
    main()
