# agents/utils/other_utils.py

def is_followup(user_query: str) -> bool:
    followup_keywords = [
        "nữa", "tiếp theo", "còn không", "có cái nào", 
        "rẻ hơn", "gần hơn", "cao hơn", "thấp hơn", 
        "ở khu khác", "có hình ảnh không", "diện tích lớn hơn"
    ]
    return any(keyword in user_query.lower() for keyword in followup_keywords)

def display_reasoning(plan: dict):
    print("\n🧠 Agent Reasoning Trace:")
    print(f"  🔹 Query after Rewrite: {plan.get('rewrite_query', 'N/A')}")
    print(f"  🔹 Retrieval Method: {plan.get('retrieval_method', 'N/A')}")
    print(f"  🔹 Reranker Model: {plan.get('reranker', 'N/A')}")
    print(f"  🔹 Reasoning Summary: {plan.get('reasoning', 'N/A')}")
    print("-" * 50)


def evaluate_results(results: list[str], min_results: int = 3) -> bool:
    """
    Đánh giá kết quả retrieval có ổn không.

    Args:
        results (list[str]): List kết quả truy vấn.
        min_results (int): Số lượng kết quả tối thiểu mong muốn.

    Returns:
        bool: True nếu đủ tốt, False nếu cần retry.
    """
    if not results or len(results) < min_results:
        return False
    
    # Có thể thêm kiểm tra content nếu muốn (ví dụ keyword missing)
    return True

def format_reasoning_markdown(plan: dict) -> str:
    """
    Format reasoning plan into a nice markdown block for display.
    """
    reasoning_text = f"### Reasoning Plan\n"
    for key, value in plan.items():
        reasoning_text += f"**{key}:** {value}\n\n"
    return reasoning_text

def rewrite_query_simple(query: str) -> str:
    query = query.strip()
    if not query.endswith("?"):
        query += "?"
    if not query.lower().startswith("find") and not query.lower().startswith("list"):
        query = "Find flats: " + query
    return query
