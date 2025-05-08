# === agents/utils/intent_detector.py ===
def is_advisory_query(query: str) -> bool:
    advisory_keywords = ["tư vấn", "gợi ý", "recommend", "suggest", "help me choose", "advise me"]
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in advisory_keywords)
