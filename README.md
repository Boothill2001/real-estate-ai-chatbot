# 🏡 Real Estate AI Chatbot

An intelligent real estate assistant capable of searching for housing listings, handling fragmented user queries, and providing personalized recommendations.

## 🚀 Features
- Hybrid Retrieval (FAISS + BM25)
- Query Rewriting and Relaxation
- Context Memory (Slot Filling)
- Reasoning Trace
- Clarification Questioning
- Personalized Re-ranking based on feedback
- Cloud-native Deployment (GCP Cloud Run + GCS)
- Production-ready Dockerized Backend
- Polished Streamlit Frontend (Auto-Scroll + Suggested Questions + Loading Animation)

## 🛠️ Tech Stack
- Python 3.11
- FastAPI, Streamlit
- FAISS, BM25, Sentence Transformers
- SQLite (for feedback tracking)
- Docker, Google Cloud Platform (Cloud Run, GCS)

## 📈 Performance
- Average Query Response Time: 0.3 - 0.5 seconds
- Designed to support 1,000+ concurrent sessions

## 📷 Screenshots
### 🔹 Chatbot Frontend UI
![image](https://github.com/user-attachments/assets/b8afa153-ad64-4671-a8b0-6becc716f4da)
### 🔹 Search Results Example
![image](https://github.com/user-attachments/assets/35ca1de1-0ff3-4953-990c-1a4bfb70291e)
### 🔹 COLLECT MORE INFORMATION TO FIND THE FINAL RESULT
![image](https://github.com/user-attachments/assets/e09281ad-8815-4174-9836-05a7a4bd0d3a)

![image](https://github.com/user-attachments/assets/37ce728b-0b23-4ab3-b928-a6c6db60a66e)

## 📦 How to Run Locally
```bash
pip install -r requirements.txt
streamlit run app_frontend.py
uvicorn app:app --reload

📡 Deployment
Backend: Deployed on Google Cloud Run

Frontend: Streamlit tunneled via Cloudflared or hosted on VM

Storage: Dataset + FAISS index on GCS bucket
