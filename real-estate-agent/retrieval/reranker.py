# retrieval/reranker.py
from agents.utils.user_profile_manager import load_user_profile
import re

def rerank_candidates(query, candidates, reranker_model, session_id=None, top_k=5):
    pairs = [(query, doc) for doc in candidates]
    scores = reranker_model.predict(pairs)

    if session_id:
        profile = load_user_profile(session_id)
        if profile:
            boosted_scores = []
            for doc, score in zip(candidates, scores):
                boost = 0.0

                # --- Boost if matches Location ---
                for loc in profile.get("preferred_locations", []):
                    if loc.lower() in doc.lower():
                        boost += 0.1  # +10%

                # --- Boost if matches Room Type ---
                for room in profile.get("preferred_room_types", []):
                    if room.lower() in doc.lower():
                        boost += 0.05  # +5%

                # --- Boost if matches Price Range ---
                price_match = extract_price_from_doc(doc)
                user_min_price, user_max_price = profile.get("preferred_price_range", (0, 9999999))
                if price_match and user_min_price <= price_match <= user_max_price:
                    boost += 0.07  # +7%

                boosted_scores.append(score + boost)

            scores = boosted_scores

    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in ranked[:top_k]]

def extract_price_from_doc(doc):
    match = re.search(r'Resale Price: (\d+)', doc)
    if match:
        return int(match.group(1))
    return None
