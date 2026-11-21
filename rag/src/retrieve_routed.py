import re
import sys
from collections import Counter

from retrieve_multivendor import load_records, retrieve


VENDOR_TERMS = {
    "VMware": [
        "vmware",
        "vsphere",
        "esxi",
        "vcenter",
        "vcenter server",
        "vsphere ha",
        "datastore heartbeating",
    ],
    "Veeam": [
        "veeam",
        "hardened repository",
        "immutability",
        "immutable backup",
        "backup repository",
    ],
}

TOP_K_PER_VENDOR = 5


def detect_vendors(question):
    question = question.lower()
    detected = []

    for vendor, terms in VENDOR_TERMS.items():
        for term in terms:
            pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"

            if re.search(pattern, question):
                detected.append(vendor)
                break

    return detected


def retrieve_routed(question, records):
    vendors = detect_vendors(question)

    if not vendors:
        return {
            "route": "global",
            "vendors": [],
            "matches": retrieve(question, records, top_k=7),
        }

    matches = []

    for vendor in vendors:
        vendor_records = [
            record for record in records
            if record["vendor"] == vendor
        ]

        vendor_matches = retrieve(
            question,
            vendor_records,
            top_k=TOP_K_PER_VENDOR,
        )

        matches.extend(vendor_matches)

    return {
        "route": "vendor",
        "vendors": vendors,
        "matches": matches,
    }


def main():
    if len(sys.argv) < 2:
        print('Usage: python rag/src/retrieve_routed.py "question"')
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    records = load_records()

    result = retrieve_routed(question, records)

    print("=== ROUTED RETRIEVAL ===")
    print("Question:", question)
    print("Route:", result["route"])
    print("Detected vendors:", result["vendors"] or "None")
    print("Total matches:", len(result["matches"]))

    counts = Counter(
        match["vendor"]
        for match in result["matches"]
    )
    print("Vendor distribution:", dict(counts))

    for rank, match in enumerate(result["matches"], 1):
        print("\n" + "-" * 65)
        print(
            f"#{rank} "
            f"vendor={match['vendor']} "
            f"page={match['page']} "
            f"chunk={match['chunk_id']} "
            f"score={match['score']:.3f}"
        )
        print("Source:", match["source"])
        print("Text:", match["text"][:250])


if __name__ == "__main__":
    main()
