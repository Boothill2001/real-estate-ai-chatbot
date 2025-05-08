# context_memory.py

class ContextMemory:
    def __init__(self):
        self.slots = {
            "location": None,
            "room_type": None,
            "price": None,
        }

    def update(self, query: str):
        """Parse query and update slots"""
        query_lower = query.lower()

        # Update location
        locations = ["ang mo kio", "bukit batok", "sengkang", "yishun", "pasir ris", "bedok", "woodlands"]
        for loc in locations:
            if loc in query_lower:
                self.slots["location"] = loc.title()

        # Update room type
        room_types = ["2-room", "3-room", "4-room", "5-room", "executive"]
        for room in room_types:
            if room in query_lower or room.replace("-", " ") in query_lower:
                self.slots["room_type"] = room.upper()

        # Update price
        import re
        price_match = re.search(r"(\d{2,3})(k|K)", query)
        if price_match:
            price_value = int(price_match.group(1)) * 1000
            self.slots["price"] = price_value

    def is_ready(self):
        """Check if all required slots are filled"""
        return self.slots["location"] and self.slots["room_type"] and self.slots["price"]

    def assemble_query(self):
        """Assemble a full query"""
        if not self.is_ready():
            return None
        return f"Find {self.slots['room_type']} flats in {self.slots['location']} under {self.slots['price']:,} SGD"

    def reset(self):
        """Reset memory after completing"""
        self.slots = {
            "location": None,
            "room_type": None,
            "price": None,
        }
