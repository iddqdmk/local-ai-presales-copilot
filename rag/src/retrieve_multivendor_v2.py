import sys

from retrieve_multivendor import load_records, retrieve
from retrieve_dell import retrieve_dell
from retrieve_routed import detect_vendors as detect_existing_vendors
import re


def detect_vendors(question):
    vendors = list(detect_existing_vendors(question) or [])

    if re.search(
        r"\b(dell|poweredge|powerstore|idrac)\b",
        question,
        flags=re.IGNORECASE,
    ):
        if "Dell" not in vendors:
            vendors.append("Dell")

    return vendors

from query_expansion import expand_query

TOP_K_PER_VENDOR = 5
GLOBAL_TOP_K = 7


def retrieve_v2(question, records):
    vendors = detect_vendors(question)

    if not vendors:
        return {
            "route": "global",
            "vendors": [],
            "matches": retrieve(
                question,
                records,
                top_k=GLOBAL_TOP_K,
            ),
            "expansion_rules": {},
        }

    matches = []
    expansion_rules = {}

    for vendor in vendors:
        vendor_records = [
            record
            for record in records
            if record["vendor"] == vendor
        ]

        expanded_question, rule = expand_query(
            question,
            vendor,
        )

        expansion_rules[vendor] = rule

        if vendor == "Dell":
            vendor_matches = retrieve_dell(
                expanded_question,
                vendor_records,
            )
        else:
            vendor_matches = retrieve(
                expanded_question,
                vendor_records,
                top_k=TOP_K_PER_VENDOR,
            )

        matches.extend(vendor_matches)

    return {
        "route": "vendor",
        "vendors": vendors,
        "matches": matches,
        "expansion_rules": expansion_rules,
    }


def main():
    if len(sys.argv) < 2:
        print(
            'Usage: python rag/src/retrieve_multivendor_v2.py "question"'
        )
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    records = load_records()

    result = retrieve_v2(question, records)

    print("=== MULTI-VENDOR RETRIEVAL V2 ===")
    print("Question:", question)
    print("Route:", result["route"])
    print("Vendors:", result["vendors"])
    print("Expansion rules:", result["expansion_rules"])
    print("Total matches:", len(result["matches"]))

    for rank, record in enumerate(result["matches"], 1):
        print("\n" + "-" * 65)
        print(
            f"#{rank} "
            f"vendor={record['vendor']} "
            f"page={record['page']} "
            f"chunk={record['chunk_id']} "
            f"score={record['score']:.3f}"
        )
        print("Source:", record["source"])
        print("Text:", record["text"][:250])


if __name__ == "__main__":
    main()
