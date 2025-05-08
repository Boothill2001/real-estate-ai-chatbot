# === agents/utils/recommender.py ===
import re
import pandas as pd
def parse_listing(doc):
    price_match = re.search(r"Resale Price: (\d+)", doc)
    size_match = re.search(r"Size: ([\d.]+)", doc)
    lease_match = re.search(r"Lease Start: (\d+)", doc)

    price = int(price_match.group(1)) if price_match else 9999999
    size = float(size_match.group(1)) if size_match else 0
    lease = int(lease_match.group(1)) if lease_match else 1900

    return price, size, lease

def recommend_best_listing(docs):
    parsed = [(doc, *parse_listing(doc)) for doc in docs]
    sorted_docs = sorted(parsed, key=lambda x: (x[1], -x[2], -x[3]))
    top_recommendations = [doc[0] for doc in sorted_docs[:2]]
    return top_recommendations
    
def suggest_top_picks(df: pd.DataFrame, location: str = None) -> str:
    filtered = df.copy()

    if location:
        filtered = filtered[filtered['town'].str.lower() == location.lower()]

    if filtered.empty:
        return "❌ Sorry, no flats found to suggest as Top Picks."

    avg_price = filtered['resale_price'].mean()
    picks = filtered[filtered['resale_price'] <= avg_price]

    if 'lease_commence_date' in filtered.columns:
        picks = picks[picks['lease_commence_date'] >= 2010]

    picks = picks[['street_name', 'flat_type', 'resale_price']].sort_values(by='resale_price').head(5)

    response = "🏡 Top Picks for you:\n\n"
    for idx, row in picks.iterrows():
        response += f"- **{row['flat_type']} at {row['street_name']}**: ${row['resale_price']:,.0f} SGD\n"

    return response
