import json
import re
import sys
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "knowledge/sources.json"

TOP_K = 7


def tokenize(text):
    return re.findall(r"[a-zа-яё0-9]+", text.lower())


def load_records():
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    records = []

    for document in catalog["documents"]:
        if document["status"] != "active":
            continue

        index_path = ROOT / document["index_path"]
        index = json.loads(index_path.read_text(encoding="utf-8"))

        for record in index["records"]:
            records.append({
                **record,
                "vendor": document["vendor"],
                "product": document["product"],
                "document_id": document["id"],
            })

    return records


def retrieve(question, records, top_k=TOP_K):
    corpus = [tokenize(record["text"]) for record in records]

    bm25 = BM25Okapi(corpus)
    scores = bm25.get_scores(tokenize(question))

    ranked = np.argsort(-scores, kind="stable")[:top_k]

    return [
        {
            **records[int(idx)],
            "score": float(scores[idx]),
        }
        for idx in ranked
    ]


def main():
    if len(sys.argv) < 2:
        print('Usage: python rag/src/retrieve_multivendor.py "question"')
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    records = load_records()

    print("=== MULTI-VENDOR RETRIEVAL ===")
    print("Total records:", len(records))
    print("Question:", question)

    matches = retrieve(question, records)

    for rank, match in enumerate(matches, 1):
        print("\n" + "-" * 65)
        print(
            f"#{rank} "
            f"vendor={match['vendor']} "
            f"page={match['page']} "
            f"chunk={match['chunk_id']} "
            f"score={match['score']:.3f}"
        )
        print("Source:", match["source"])
        print("Text:", match["text"][:350])


if __name__ == "__main__":
    main()
