# app.py - Real Estate Chatbot Backend (Final English Version)

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, CrossEncoder
from rank_bm25 import BM25Okapi
import pandas as pd
import numpy as np
import faiss
import sqlite3
import time
from agents.utils.context_memory import ContextMemory
from agents.utils.query_analyzer import detect_missing_info
from agents.utils.recommender import recommend_best_listing
from agents.utils.other_utils import is_followup, display_reasoning, format_reasoning_markdown, rewrite_query_simple
from agents.utils.price_calculator import is_price_query, is_filter_query, extract_location_room, calculate_average_price, handle_filter_query
from agents.utils.intent_detector import is_advisory_query
from agents.utils.advisory_generator import generate_advisory
from agents.utils.mcp_manager import MCPManager
from agents.self_correction import needs_retry, rewrite_query
from agents.planner import plan as planner
from retrieval.faiss_bm25 import hybrid_search
from retrieval.reranker import rerank_candidates
from agents.utils.user_profile_manager import update_user_profile

app = FastAPI(title="Real Estate Chatbot API")

# === Load Models and Indexes ===
print("🔥 Loading models and indexes...")
df_all = pd.read_csv("data/processed_subset.csv")
texts = df_all["text_for_embedding"].tolist()
embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
reranker_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
faiss_index = faiss.read_index("faiss_index_subset.index")
bm25_index = BM25Okapi([doc.lower().split() for doc in texts])

mcp_manager = MCPManager()

# === Initialize Feedback DB ===
def init_feedback_db():
    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            query TEXT,
            feedback_score INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_feedback_db()

# === Request Schemas ===
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    session_id: str

class FeedbackRequest(BaseModel):
    session_id: str
    query: str
    feedback_score: int

# === Health Check ===
@app.get("/")
def health_check():
    return {"message": "Real Estate Chatbot Backend is running ✅"}

# === /ask Endpoint ===
# In-memory store per session
session_contexts = {}

@app.post("/ask")
def ask_question(req: QueryRequest):
    session_id = req.session_id

    # Initialize context if new
    if session_id not in session_contexts:
        session_contexts[session_id] = ContextMemory()

    memory = session_contexts[session_id]
    query = req.query

    # Step 1: Update memory with new query
    memory.update(query)

    # Step 2: If not ready, ask for missing info
    if not memory.is_ready():
        missing = []
        for slot, value in memory.slots.items():
            if value is None:
                missing.append(slot.replace("_", " ").title())
        clarification = f"❓ Please provide: {', '.join(missing)}"
        return {
            "query": query,
            "documents": [clarification],
            "plan_steps": ["❓ Missing info detected."]
        }

    # Step 3: Assemble full query if ready
    final_query = memory.assemble_query()

    # Step 4: Proceed search as normal
    reasoning_steps = []
    candidates = hybrid_search(final_query, embedder, faiss_index, bm25_index, texts, top_k=10)
    top_docs = rerank_candidates(final_query, candidates, reranker_model, session_id=session_id, top_k=req.top_k)
    reasoning_steps.append(f"🔵 Step 1: Search with assembled query ➔ {len(top_docs)} results found.")

    # Reset memory after complete
    memory.reset()

    if not top_docs:
        return {
            "query": final_query,
            "documents": ["❗ Sorry, no flats found matching your criteria."],
            "plan_steps": reasoning_steps
        }

    return {
        "query": final_query,
        "documents": top_docs,
        "plan_steps": reasoning_steps
    }

# === /query Endpoint (Agent Search) ===
@app.post("/query")
async def query_agent(user_query: str = Query(...), session_id: str = Query(...)):
    try:
        context = mcp_manager.load_context(session_id)

        if context and is_followup(user_query):
            user_query = context["last_query"] + " " + user_query

        planned_query = planner(user_query)["planned_query"]
        candidates = hybrid_search(planned_query, embedder, faiss_index, bm25_index, texts, top_k=10)
        top_results = rerank_candidates(planned_query, candidates, reranker_model, session_id=session_id, top_k=5)

        plan = {
            "rewrite_query": planned_query,
            "retrieval_method": "Hybrid FAISS + BM25",
            "reranker": "cross-encoder-v1",
            "reasoning": "Context-aware search if follow-up detected."
        }

        mcp_manager.save_context(session_id, user_query, plan, top_results)
        markdown_reasoning = format_reasoning_markdown(plan)

        return {"results": top_results, "plan": plan, "reasoning_markdown": markdown_reasoning}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === Feedback ===
@app.post("/feedback")
def collect_feedback(req: FeedbackRequest):
    try:
        conn = sqlite3.connect("feedback.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO feedback (session_id, query, feedback_score)
            VALUES (?, ?, ?)
        ''', (req.session_id, req.query, req.feedback_score))
        conn.commit()
        conn.close()

        if req.feedback_score == 1:
            context = mcp_manager.load_context(req.session_id)
            if context:
                update_user_profile(req.session_id, req.query, context.get("last_results", []))

        return {"message": "Feedback recorded successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
