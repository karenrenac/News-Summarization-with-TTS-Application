# app.py

import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"  # Update to your deployed backend URL on Hugging Face Spaces

st.set_page_config(page_title="📰 News Sentiment Analyzer", layout="centered")
st.title("📰 Company News Analyzer with Hindi Audio Report")

st.markdown("""
This app fetches news articles about a company, summarizes them, analyzes sentiment, compares coverage, and generates a Hindi audio summary 🎧.
""")

# ------------------- Input Section -------------------
company = st.text_input("Enter Company Name", "")

if st.button("Run Analysis"):
    if not company.strip():
        st.warning("Please enter a valid company name.")
    else:
        st.info("Running full pipeline via `/analyze` API...")

        try:
            response = requests.post(f"{API_BASE_URL}/analyze", json={"company_name": company})
            
            if response.status_code == 200:
                data = response.json()

                st.subheader(f"📌 Company: {data.get('Company', '')}")

                for i, article in enumerate(data.get("Articles", []), 1):
                    st.markdown(f"### Article {i}")
                    st.markdown(f"**Title:** {article.get('Title', '')}")
                    st.markdown(f"**Summary:** {article.get('Summary', '')}")
                    st.markdown(f"**Sentiment:** {article.get('Sentiment', '')}")
                    st.markdown(f"**Topics:** {', '.join(article.get('Topics', []))}")

                st.subheader("📊 Comparative Sentiment Score")
                st.json(data.get("Comparative Sentiment Score", {}))

                st.subheader("🧠 Final Sentiment Summary")
                st.write(data.get("Final Sentiment Analysis", ""))

                st.subheader("🎧 Hindi Audio Report")
                audio_path = data.get("Audio", "")
                try:
                    with open(audio_path, 'rb') as f:
                        audio_bytes = f.read()
                        st.audio(audio_bytes, format="audio/mp3")
                except Exception as e:
                    st.error(f"Could not load audio file: {e}")

            else:
                st.error(f"Error from API: {response.json().get('detail', 'Unknown error')}")

        except Exception as e:
            st.error(f"Failed to connect to backend API: {str(e)}")
