# comparative_analysis.py

from collections import Counter
import statistics

def sentiment_distribution(articles):
    """
    Returns sentiment breakdown counts and average sentiment score.
    """
    sentiments = [a['sentiment'] for a in articles]
    scores = [a['sentiment_score'] for a in articles if isinstance(a['sentiment_score'], (int, float))]

    distribution = Counter(sentiments)
    avg_score = round(statistics.mean(scores), 3) if scores else 0.0

    return distribution, avg_score


def top_articles_by_sentiment(articles, top_n=3):
    """
    Returns top N positive and top N negative articles based on sentiment_score.
    """
    sorted_articles = sorted(articles, key=lambda x: x['sentiment_score'], reverse=True)
    top_positive = [a for a in sorted_articles if a['sentiment'] == "Positive"][:top_n]
    top_negative = [a for a in sorted_articles if a['sentiment'] == "Negative"][-top_n:]

    return top_positive, top_negative


def keyword_frequency(articles, top_n=10):
    """
    Extracts most frequent keywords from article titles.
    """
    import re
    words = []

    for article in articles:
        title = article.get('title', '')
        words += re.findall(r'\b[a-zA-Z]{4,}\b', title.lower())  # take only words >=4 characters

    # Remove common stopwords
    stopwords = {"about", "from", "with", "this", "that", "which", "have", "been", "they", "will", "their", "into"}
    filtered_words = [word for word in words if word not in stopwords]

    return Counter(filtered_words).most_common(top_n)


def generate_analysis_report(articles):
    """
    Prints a clean comparative analysis report in assignment-style format.
    """
    total_articles = len(articles)
    dist, avg_score = sentiment_distribution(articles)
    top_pos, top_neg = top_articles_by_sentiment(articles)
    keywords = keyword_frequency(articles)

    print("\n======================= Comparative Analysis =======================\n")

    print(f"Total Articles Fetched: {total_articles}\n")

    print("Sentiment Distribution:")
    print(f"Positive: {dist.get('Positive', 0)}")
    print(f"Neutral : {dist.get('Neutral', 0)}")
    print(f"Negative: {dist.get('Negative', 0)}")

    print(f"\nAverage Sentiment Score: {avg_score}\n")

    print("Top Positive Articles:")
    if top_pos:
        for article in top_pos:
            print(f"- Title: {article['title']}")
            print(f"  Sentiment Score: {article['sentiment_score']}\n")
    else:
        print("  No positive articles found.\n")

    print("Top Negative Articles:")
    if top_neg:
        for article in top_neg:
            print(f"- Title: {article['title']}")
            print(f"  Sentiment Score: {article['sentiment_score']}\n")
    else:
        print("  No negative articles found.\n")

    print("Most Frequent Keywords in Titles:")
    for word, count in keywords:
        print(f"- {word}: {count} times")

    print("\n====================================================================\n")
