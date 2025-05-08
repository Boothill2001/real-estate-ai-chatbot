# session_memory.py – Simple User Session Memory Manager

import time

# Memory structure: {session_id: {"history": [(query, response)], "last_active": timestamp}}
session_memory = {}

# Memory config
SESSION_TIMEOUT = 600  # seconds = 10 minutes

def add_to_memory(session_id, query, response):
    now = time.time()
    if session_id not in session_memory:
        session_memory[session_id] = {"history": [], "last_active": now}
    session_memory[session_id]["history"].append((query, response))
    session_memory[session_id]["last_active"] = now

def get_recent_context(session_id, n_turns=2):
    if session_id not in session_memory:
        return []
    history = session_memory[session_id]["history"]
    return history[-n_turns:]  # get last n_turns

def reset_session(session_id):
    if session_id in session_memory:
        del session_memory[session_id]

def cleanup_sessions():
    now = time.time()
    to_delete = []
    for session_id, session_data in session_memory.items():
        if now - session_data["last_active"] > SESSION_TIMEOUT:
            to_delete.append(session_id)
    for sid in to_delete:
        del session_memory[sid]
