# agents/planner.py

from typing import Dict

def plan(user_query: str) -> Dict[str, str]:
    """
    Mini planner: Simply returns planned_query.
    In production: You can add LLM or rule-based planning here.

    Args:
        user_query (str): Original user query.

    Returns:
        Dict[str, str]: Planned query dictionary.
    """
    planned_query = user_query.strip()
    return {
        "planned_query": planned_query,
        "plan_steps": ["analyze", "reformulate", "search"]
    }
