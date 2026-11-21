import re


FAILURE_DETECTION_TERMS = [
    "detect",
    "detection",
    "distinguish",
    "heartbeat",
    "heartbeating",
    "network isolation",
    "network isolated",
    "host liveness",
]

FAILURE_CONTEXT = (
    " primary host secondary host "
    "network heartbeats datastore heartbeating "
    "ICMP host liveness failure detection"
)


def contains_term(text, term):
    pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"
    return bool(re.search(pattern, text))


def expand_query(question, vendor):
    if vendor != "VMware":
        return question, "unchanged"

    normalized = question.lower()

    if any(
        contains_term(normalized, term)
        for term in FAILURE_DETECTION_TERMS
    ):
        return question + FAILURE_CONTEXT, "failure_detection"

    return question, "unchanged"
