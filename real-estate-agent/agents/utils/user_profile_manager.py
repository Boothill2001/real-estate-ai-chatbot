# agents/utils/user_profile_manager.py
import os
import pickle

PROFILE_FOLDER = "user_profiles"

os.makedirs(PROFILE_FOLDER, exist_ok=True)

def get_profile_path(session_id):
    return os.path.join(PROFILE_FOLDER, f"{session_id}.pkl")

def update_user_profile(session_id, query, documents):
    profile = load_user_profile(session_id)

    for doc in documents:
        if "YISHUN" in doc.upper():
            profile["preferred_locations"].add("Yishun")
        if "BUKIT BATOK" in doc.upper():
            profile["preferred_locations"].add("Bukit Batok")
        if "PASIR RIS" in doc.upper():
            profile["preferred_locations"].add("Pasir Ris")
        if "SENGKANG" in doc.upper():
            profile["preferred_locations"].add("Sengkang")
        if "ANG MO KIO" in doc.upper():
            profile["preferred_locations"].add("Ang Mo Kio")
        if "BEDOK" in doc.upper():
            profile["preferred_locations"].add("Bedok")

        if "4 ROOM" in doc.upper():
            profile["preferred_room_types"].add("4 ROOM")
        if "5 ROOM" in doc.upper():
            profile["preferred_room_types"].add("5 ROOM")
        if "EXECUTIVE" in doc.upper():
            profile["preferred_room_types"].add("EXECUTIVE")

    # Infer preferred price range from query
    if "under 400k" in query.lower():
        profile["preferred_price_range"] = (0, 400000)
    elif "under 600k" in query.lower():
        profile["preferred_price_range"] = (0, 600000)
    elif "under 800k" in query.lower():
        profile["preferred_price_range"] = (0, 800000)

    with open(get_profile_path(session_id), "wb") as f:
        pickle.dump(profile, f)

def load_user_profile(session_id):
    try:
        with open(get_profile_path(session_id), "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {
            "preferred_locations": set(),
            "preferred_price_range": (0, 9999999),
            "preferred_room_types": set()
        }
