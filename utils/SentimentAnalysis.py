from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import os

# Load model and tokenizer
BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "hf_model")

TOKENIZER_PATH = os.path.join(BASE_PATH, "tokenizer")
MODEL_PATH = os.path.join(BASE_PATH, "model")

tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

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
