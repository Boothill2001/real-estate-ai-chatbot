# monitoring_dashboard.py – Real Estate Chatbot Feedback Monitoring (Pro Version)

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# 🚀 Page Setup
st.set_page_config(page_title="📊 Real Estate Chatbot Monitoring", layout="wide")
st.title("📊 Real Estate Chatbot Monitoring Dashboard")

# 📂 Load feedback.db
@st.cache_data
def load_feedback():
    conn = sqlite3.connect("feedback.db")
    df = pd.read_sql_query("SELECT * FROM feedback", conn)
    conn.close()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

df = load_feedback()

# 📈 KPIs
col1, col2, col3 = st.columns(3)
col1.metric("📨 Total Feedback", len(df))
like_ratio = df[df['feedback_score'] == 1].shape[0] / len(df) * 100 if len(df) > 0 else 0
col2.metric("👍 Like Rate", f"{like_ratio:.1f}%")
dislike_ratio = df[df['feedback_score'] == 0].shape[0] / len(df) * 100 if len(df) > 0 else 0
col3.metric("👎 Dislike Rate", f"{dislike_ratio:.1f}%")

st.markdown("---")

# 🥧 Pie Chart: Like vs Dislike
st.subheader("🥧 Like vs Dislike Distribution")
fig_pie = px.pie(
    names=["Like", "Dislike"],
    values=[df['feedback_score'].tolist().count(1), df['feedback_score'].tolist().count(0)],
    color_discrete_sequence=["green", "red"],
    hole=0.4
)
st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# 📈 Line Chart: Feedback Over Time
st.subheader("📈 Feedback Activity Over Time")
df_time = df.copy()
df_time['date'] = df_time['timestamp'].dt.date
feedback_over_time = df_time.groupby('date').size().reset_index(name='count')
fig_line = px.line(feedback_over_time, x='date', y='count', markers=True)
st.plotly_chart(fig_line, use_container_width=True)

st.markdown("---")

# 🏆 Top 5 Liked Queries
st.subheader("🏆 Top 5 Queries (Most Liked)")
df_like = df[df['feedback_score'] == 1]
top_queries = df_like['query'].value_counts().head(5).reset_index()
top_queries.columns = ["Query", "Likes"]
st.dataframe(top_queries, use_container_width=True)

st.markdown("---")

# 🕒 Recent Feedbacks
st.subheader("🕒 Recent Feedback Activity")
recent_df = df.sort_values(by='timestamp', ascending=False).head(10)
recent_df_display = recent_df[["timestamp", "query", "feedback_score"]]
recent_df_display['feedback_score'] = recent_df_display['feedback_score'].map({1: "👍 Like", 0: "👎 Dislike"})
st.dataframe(recent_df_display, use_container_width=True)

# 📜 Footer
st.markdown("---")
st.caption("© 2025 Real Estate RAG Chatbot - Monitoring Dashboard")
