from NewsScrapper import get_news_articles
from ComparitiveAnalysis import generate_structured_analysis
import json

if __name__ == "__main__":
    company = input("Enter company name: ")
    articles = get_news_articles(company, limit=10)

    for idx, article in enumerate(articles):
        print(f"\n--- Article {idx + 1} ---")
        print(f"Title       : {article['title']}")
        print(f"Summary     : {article['summary']}")
        print(f"Sentiment   : {article['sentiment']} (Score: {article['sentiment_score']})")
        print(f"Publish Date: {article['publish_date']}")
        print(f"URL         : {article['url']}")

    structured = generate_structured_analysis(company, articles)

    print("\n==================== Final Structured Analysis ====================\n")
    print(json.dumps(structured, indent=4))

