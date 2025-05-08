# self_correction.py
import random

def needs_retry(documents):
    if isinstance(documents, list) and len(documents) > 0:
        if isinstance(documents[0], str) and "sorry" not in documents[0].lower():
            return False
    return True

def rewrite_query(query):
    # Very basic rewriter for now
    synonyms = {
        "affordable": ["cheap", "low cost", "budget"],
        "executive": ["premium", "luxury"],
        "under": ["below"],
        "flats": ["apartments", "units"]
    }
    rewritten = query
    for word, syns in synonyms.items():
        if word in query.lower():
            rewritten = rewritten.replace(word, random.choice(syns))
    return rewritten

def relax_query(query):
    # Relax some constraints manually
    relaxed = query
    if "under 400k" in query.lower():
        relaxed = relaxed.lower().replace("under 400k", "under 600k")
    if "after 2015" in query.lower():
        relaxed = relaxed.lower().replace("after 2015", "after 2010")
    return relaxed
