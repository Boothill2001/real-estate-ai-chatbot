# agents/core/agent_handler.py (ví dụ hoặc wherever you handle queries)

# from agents.planner import llm_planner
# from agents.self_correction import needs_retry, rewrite_query
# from retrieval.faiss_bm25 import retrieve_documents

# def handle_query(user_query: str, top_k: int = 5):
#     # Step 1: Plan query
#     plan = llm_planner.plan(user_query)
    
#     # Step 2: Retrieve documents
#     results = retrieve_documents(plan["planned_query"], top_k=top_k)
    
#     # Step 3: Evaluate results
#     if needs_retry(results):
#         print("🔄 Weak results detected, rewriting query...")

#         # Step 4: Rewrite query
#         rewritten_query = rewrite_query(user_query)

#         # Step 5: Replan with rewritten query
#         plan = llm_planner.plan(rewritten_query)

#         # Step 6: Retrieve again
#         results = retrieve_documents(plan["planned_query"], top_k=top_k)

    #    # Step 7: Final check
    #     if needs_retry(results):
    #         print("⚠️ Retry failed. Returning fallback message.")
    #         return ["Sorry, I couldn't find good results even after retrying."]
    
    # # Step 8: Return good results
    # return results
