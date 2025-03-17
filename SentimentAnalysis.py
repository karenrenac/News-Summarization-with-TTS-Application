# sentiment_analysis.py

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Load model and tokenizer once globally
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Set up sentiment pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Label mapping from model index or label to human-readable label
LABEL_MAP = {
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive",
    "NEGATIVE": "Negative",
    "NEUTRAL": "Neutral",
    "POSITIVE": "Positive"
}

def get_sentiment(text):
    """
    Performs sentiment analysis on the input text using a transformer model.

    Args:
        text (str): The article content or summary.

    Returns:
        dict: Sentiment label and score
    """
    try:
        result = sentiment_pipeline(text[:512])[0]  # Limit to 512 tokens
        raw_label = result['label'].strip().upper()
        score = round(result['score'], 3)

        # Try to get mapped label first
        sentiment = LABEL_MAP.get(raw_label)

        # Fallback score-based sentiment classification
        if not sentiment:
            if score >= 0.6:
                sentiment = "Positive"
            elif score <= 0.4:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"

        return {
            "sentiment": sentiment,
            "score": score
        }

    except Exception as e:
        print(f"[ERROR] Sentiment analysis failed: {e}")
        return {
            "sentiment": "Unknown",
            "score": 0.0
        }
