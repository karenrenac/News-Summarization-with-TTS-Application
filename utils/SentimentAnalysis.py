from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Load model and tokenizer
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Create pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Label map – handle both label types
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
    Returns: dict with sentiment label and score
    """
    try:
        result = sentiment_pipeline(text[:512])[0]
        raw_label = result['label'].strip().upper()
        score = round(result['score'], 3)

        sentiment = LABEL_MAP.get(raw_label)
        if not sentiment:
            if score >= 0.75:
                sentiment = "Positive"
            elif score <= 0.55:
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
