# News Summarization and Sentiment Analysis Application

## Overview

This application performs news summarization, sentiment analysis, comparative analysis, and generates Hindi audio summaries using text-to-speech. Users can input a company name and receive a structured sentiment report, along with a playable audio output in Hindi.

The solution is designed as part of an internship assignment to demonstrate end-to-end software development involving web scraping, NLP, API design, and deployment.

## Features

- Extract news articles related to a given company using Bing RSS feeds.
- Summarize each article using LexRank extractive summarization.
- Perform sentiment analysis using a transformer-based RoBERTa model.
- Conduct comparative sentiment and topic analysis across articles.
- Generate a Hindi audio summary using gTTS.
- Expose APIs via FastAPI for frontend-backend interaction.
- Simple frontend interface using Streamlit.
- Deployable via Docker or on Hugging Face Spaces.