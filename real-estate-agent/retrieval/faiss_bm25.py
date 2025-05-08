# retrieval/faiss_bm25.py

from typing import List

# retrieval/hybrid.py

import numpy as np

def hybrid_search(query, embedder, faiss_index, bm25_index, texts, top_k=10):
    """
    Perform hybrid search using both FAISS (dense retrieval) and BM25 (sparse retrieval).
    
    Args:
        query (str): User input query.
        embedder (SentenceTransformer): Embedding model to encode query.
        faiss_index (faiss.Index): FAISS index for dense retrieval.
        bm25_index (BM25Okapi): BM25 index for sparse retrieval.
        texts (List[str]): List of documents.
        top_k (int): Number of top documents to return.
    
    Returns:
        List[str]: Top-k retrieved documents combined from FAISS and BM25.
    """
    # --- Dense search with FAISS ---
    query_vector = embedder.encode([query], normalize_embeddings=True)
    D, I = faiss_index.search(np.array(query_vector).astype('float32'), top_k)
    faiss_docs = [texts[idx] for idx in I[0] if idx != -1]

    # --- Sparse search with BM25 ---
    bm25_results = bm25_index.get_top_n(query, texts, n=top_k)

    # --- Merge results ---
    hybrid_results = faiss_docs + bm25_results

    # Remove duplicates while preserving order
    seen = set()
    unique_results = []
    for doc in hybrid_results:
        if doc not in seen:
            unique_results.append(doc)
            seen.add(doc)
    
    return unique_results[:top_k]

# Giả sử FAISS index hoặc BM25 index đã được load vào đây (mock)
dummy_database = [
    "Affordable 4-room flat in Yishun under 400k SGD.",
    "Executive flat in Pasir Ris for under 800k SGD.",
    "5-room flat in Bukit Batok priced at 580k SGD.",
    "Flats with lease start after 2015 in Sengkang.",
    "Average price of 3-room flats in Ang Mo Kio is 400k SGD."
]

def retrieve_documents(query: str, top_k: int = 5) -> List[str]:
    """
    Mock retrieval logic: Search documents containing any keyword from query.
    In production: Replace this with real FAISS/BM25 search.

    Args:
        query (str): User's search query
        top_k (int): Number of results to return

    Returns:
        List[str]: Retrieved documents
    """
    matched_docs = [doc for doc in dummy_database if any(word.lower() in doc.lower() for word in query.split())]
    return matched_docs[:top_k]
