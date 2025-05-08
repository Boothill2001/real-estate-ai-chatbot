# price_calculator.py - Utilities for Price Analysis and Filter

import re
import pandas as pd

def is_price_query(query: str) -> bool:
    """Detect if the query is about average price."""
    query_lower = query.lower()
    keywords = ["average price", "mean price", "median price", "giá trung bình"]
    return any(keyword in query_lower for keyword in keywords)

def extract_location_room(query: str) -> tuple:
    """Simple extractor for location and room type."""
    locations = ["ang mo kio", "bukit batok", "sengkang", "yishun", "pasir ris", "bedok", "woodlands"]
    room_types = ["2-room", "3-room", "4-room", "5-room", "executive"]

    found_location = None
    found_room = None
    query_lower = query.lower()

    for loc in locations:
        if loc in query_lower:
            found_location = loc.title()
            break

    for room in room_types:
        if room in query_lower:
            found_room = room.upper()
            break

    return found_location, found_room

def calculate_average_price(location: str, room_type: str, df: pd.DataFrame) -> str:
    """Calculate the average resale price for given location and room type."""
    filtered = df[
        (df['town'].str.lower() == location.lower()) &
        (df['flat_type'].str.upper() == room_type.upper())
    ]

    if len(filtered) < 3:
        return "❌ Sorry, not enough data to accurately calculate average price. 🏡"

    avg_price = round(filtered['resale_price'].mean(), 2)
    return f"📈 The average price for **{room_type}** flats in **{location}** is **${avg_price:,.0f} SGD**."

def is_filter_query(query: str) -> bool:
    """Detect if the query requests flats under a certain price."""
    query_lower = query.lower()
    return any(word in query_lower for word in ["under", "below", "less than", "cheaper than"])

def handle_filter_query(query: str, df: pd.DataFrame) -> str:
    """Handle queries that filter flats under a specified price."""
    location, room_type = extract_location_room(query)

    if not location or not room_type:
        return "❓ Please specify both the location and room type (e.g., '4-room in Yishun')."

    price_match = re.search(r"(under|below|less than|cheaper than)\s?([\d,]+)", query.lower())
    if not price_match:
        return "❓ Please specify a price limit (e.g., 'under 600k')."

    price_str = price_match.group(2).replace(",", "")
    try:
        price_limit = int(price_str) * 1000  # 600k => 600,000
    except:
        return "❓ Could not parse the price. Please enter correctly (e.g., 'under 600k')."

    filtered = df[
        (df['town'].str.lower() == location.lower()) &
        (df['flat_type'].str.upper() == room_type.upper()) &
        (df['resale_price'] <= price_limit)
    ]

    if filtered.empty:
        return f"❌ No {room_type} flats found in {location} below **${price_limit:,} SGD**."

    results = filtered[['street_name', 'resale_price']].head(5)

    response = f"🏡 **Found {len(results)} {room_type} flats in {location} under ${price_limit:,.0f} SGD:**\n\n"
    for idx, row in results.iterrows():
        response += f"- 📍 **{row['street_name']}**: **${row['resale_price']:,.0f} SGD**\n"

    return response
