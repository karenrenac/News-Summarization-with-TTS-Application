# api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

from utils.NewsScrapper import get_news_articles
from utils.Summarizer import get_summary
from utils.SentimentAnalysis import get_sentiment
from utils.ComparitiveAnalysis import generate_structured_analysis, generate_sentiment_summary, topic_overlap, generate_coverage_comparisons, sentiment_distribution
from utils.TTSHindi import speak_hindi_sentiment_report

app = FastAPI()

# ------------------ MODELS ------------------ #

class CompanyRequest(BaseModel):
    company_name: str

class TextListRequest(BaseModel):
    texts: List[str]

class ArticlesRequest(BaseModel):
    articles: List[Dict]  # expecting articles with at least "title" and "summary" fields


# ------------------ ROUTES ------------------ #

@app.get("/test")
def test():
    return {"message": "Testing news Sentiment Analysis API is up and running."}


@app.get("/")
def home(company_name: str = None):
    if company_name:
        return {"message": f"Company Name: {company_name}"}
    return {"message": "News Sentiment Analysis API is up and running."}

@app.post("/news")
def fetch_news(request: CompanyRequest):
    try:
        articles = get_news_articles(request.company_name, limit=10)
        return {"articles": articles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/summary")
def summarize_articles(request: TextListRequest):
    try:
        summarized = []
        for text in request.texts:
            summary = get_summary(text)
            summarized.append({"summary": summary})
        return {"summaries": summarized}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sentiment")
def analyze_sentiments(request: TextListRequest):
    try:
        sentiments = []
        for text in request.texts:
            result = get_sentiment(text)
            sentiments.append(result)
        return {"sentiments": sentiments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compare")
def compare_articles(request: ArticlesRequest):
    try:
        articles = request.articles

        # Enrich articles with topics if not already added
        for a in articles:
            if 'topics' not in a:
                a['topics'] = []

        sentiment_dist, avg_score = sentiment_distribution(articles)
        coverage_differences = generate_coverage_comparisons(articles)
        topics = topic_overlap(articles)
        summary = generate_sentiment_summary(articles)

        return {
            "Sentiment Distribution": dict(sentiment_dist),
            "Coverage Differences": coverage_differences,
            "Topic Overlap": topics,
            "Summary": summary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tts")
def generate_tts(request: ArticlesRequest):
    try:
        sentiment_dist, _ = sentiment_distribution(request.articles)
        final_summary = generate_sentiment_summary(request.articles)

        base64_audio = speak_hindi_sentiment_report(sentiment_dist, final_summary)

        if not base64_audio:
            raise HTTPException(status_code=500, detail="TTS generation failed")

        return {"audio_base64": base64_audio}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze")
def full_pipeline_analysis(request: CompanyRequest):
    try:
        # Step 1: News Extraction
        articles = get_news_articles(request.company_name, limit=10)

        # Step 2: Full Comparative Analysis
        report = generate_structured_analysis(request.company_name, articles)

        # Step 3: Generate Hindi TTS
        sentiment_dist = report["Comparative Sentiment Score"]["Sentiment Distribution"]
        final_summary = report["Final Sentiment Analysis"]
        audio_filename = "hindisentimentreport.mp3"
        speak_hindi_sentiment_report(sentiment_dist, final_summary, filename=audio_filename)

        report["Audio"] = audio_filename

        return report

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
