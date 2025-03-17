# news_scraper.py

import requests
from bs4 import BeautifulSoup
import re
import random
import time
from SentimentAnalysis import get_sentiment
from Summarizer import get_summary


def fetch_bing_news_links(company_name, limit=10):
    """
    Fetches news article links from Bing News RSS using multiple query variations
    to reach the required article limit.
    """
    query_variants = [
        company_name,
        f"{company_name} news",
        f"{company_name} latest",
        f"{company_name} headlines",
        f"{company_name} stock",
        f"{company_name} financial",
        f"{company_name} business",
        f"{company_name} growth",
        f"{company_name} market",
        f"{company_name} performance"
    ]

    articles = []
    seen_urls = set()

    for query in query_variants:
        url = f"https://www.bing.com/news/search?q={query.replace(' ', '+')}&format=rss"
        print(f"[INFO] Querying Bing RSS: {query}")

        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f"[WARN] RSS fetch failed for query: {query}")
                continue

            soup = BeautifulSoup(response.content, features="xml")
            items = soup.find_all('item')

            for item in items:
                link = item.link.text.strip()

                if link in seen_urls:
                    continue

                title = item.title.text.strip()
                bing_summary = item.description.text.strip()
                pub_date = item.pubDate.text if item.pubDate else "Unknown"

                articles.append({
                    'title': title,
                    'summary': bing_summary,
                    'url': link,
                    'publish_date': pub_date
                })
                seen_urls.add(link)

                if len(articles) >= limit:
                    break

        except Exception as e:
            print(f"[ERROR] Failed to fetch from Bing RSS for {query}: {e}")
            continue

        if len(articles) >= limit:
            break

    print(f"[INFO] Total unique articles collected: {len(articles)}")
    return articles

def extract_article_text(url):
    """
    Extract article body text from the article URL using BS4.
    """
    try:
        headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
                'Mozilla/5.0 (X11; Linux x86_64)'
            ])
        }
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"[WARN] Skipping article {url} — status {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = " ".join(p.text for p in paragraphs)
        text = re.sub(r'\s+', ' ', text).strip()

        return text if text else None

    except Exception as e:
        print(f"[ERROR] Failed to extract article text: {e}")
        return None

def get_news_articles(company_name, limit=10):
    """
    Master function: Fetch news, extract content, add sentiment.
    Returns structured article data.
    """
    links = fetch_bing_news_links(company_name, limit)
    articles = []

    for article in links:
        print(f"[INFO] Processing article: {article['title']}")
        text = extract_article_text(article['url'])

        # Fallback to description if full article body fails
        article['text'] = text if text else article['summary']
        article['summary'] = get_summary(article['text'])
        # Sentiment analysis
        sentiment_result = get_sentiment(article['text'])
        article['sentiment'] = sentiment_result['sentiment']
        article['sentiment_score'] = sentiment_result['score']

        articles.append(article)

        time.sleep(random.uniform(1.5, 3))  # Gentle delay

    return articles
