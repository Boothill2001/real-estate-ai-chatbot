# agents/utils/query_analyzer.py

def detect_missing_info(query: str) -> list:
    missing = []
    query_lower = query.lower()

    if not any(loc in query_lower for loc in ["yishun", "bukit batok", "sengkang", "ang mo kio", "pasir ris"]):
        missing.append("khu vực")
    if "under" not in query_lower and "$" not in query_lower and "k" not in query_lower:
        missing.append("giá")
    if not any(room in query_lower for room in ["3-room", "4-room", "5-room", "executive"]):
        missing.append("loại phòng")

    return missing
def is_generic_query(query: str) -> bool:
    generic_keywords = ["find flats", "find apartment", "list flats", "show flats", "tim can ho"]
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in generic_keywords)

