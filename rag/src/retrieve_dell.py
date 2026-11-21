import re

from retrieve_multivendor import retrieve


def retrieve_dell(question, records):
    dell = [
        r for r in records
        if r["vendor"] == "Dell"
    ]

    q = question.lower()

    if "powerstore" in q:
        selected = [
            r for r in dell
            if "powerstore" in r["product"].lower()
        ]
    elif "poweredge" in q or re.search(r"\br760\b", q):
        selected = [
            r for r in dell
            if "poweredge" in r["product"].lower()
        ]
    else:
        selected = dell

    if not selected:
        return []

    queries = [question]

    if "powerstore" in q:
        if any(w in q for w in ("rack", "space", "dimension", "weight")):
            queries.append(
                "base enclosure dimensions weight rack space "
                "vertical size height width depth"
            )

        if any(w in q for w in ("power", "electric", "watt", "consumption")):
            queries.append(
                "Power requirements for x200 models "
                "1200T power consumption operating maximum"
            )

    if "poweredge" in q or re.search(r"\br760\b", q):
        if "cpu" in q or "processor" in q:
            queries.append(
                "PowerEdge R760 processor specifications "
                "Intel Xeon Scalable supported processors"
            )

        if "memory" in q or "ram" in q:
            queries.append(
                "PowerEdge R760 memory specifications "
                "DIMM slots DDR5 RDIMM"
            )

    matches = []
    seen = set()

    # Collect evidence from each aspect of the question.
    # Limit context to avoid overloading the local model.
    per_query = 3 if len(queries) > 1 else 7

    for query in queries:
        for record in retrieve(
            query,
            selected,
            top_k=per_query,
        ):
            key = (
                record["document_id"],
                record["page"],
                record["chunk_id"],
            )

            if key in seen:
                continue

            seen.add(key)
            matches.append(record)

            if len(matches) >= 9:
                return matches

    return matches
