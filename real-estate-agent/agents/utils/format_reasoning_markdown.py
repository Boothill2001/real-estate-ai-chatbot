def format_reasoning_markdown(plan: dict) -> str:
    reasoning_md = f"""
## 🤖 Agent Reasoning

**🔹 Query after Rewrite:**  
{plan.get('rewrite_query', 'N/A')}

**🔹 Retrieval Method:**  
{plan.get('retrieval_method', 'N/A')}

**🔹 Reranker Model:**  
{plan.get('reranker', 'N/A')}

**🧠 Reasoning Summary:**  
{plan.get('reasoning', 'N/A')}
"""
    return reasoning_md.strip()
