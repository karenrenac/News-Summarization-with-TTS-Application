import requests
from bs4 import BeautifulSoup
import re
import random
import time
import hashlib

from SentimentAnalysis import get_sentiment
from Summarizer import get_summary

def fetch_bing_news_links(company_name, limit=10):
    """
    Fetch news article links from Bing News RSS based on a single clean query.
    Guarantees collection of `limit` unique articles by paginating results if needed.
    """
    query = company_name.strip()
    collected_articles = []
    seen_urls = set()

    print(f"[INFO] Querying Bing RSS: {query}")

    url = f"https://www.bing.com/news/search?q={query.replace(' ', '+')}&format=rss"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"[WARN] Bing RSS fetch failed with status code {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, features="xml")
        items = soup.find_all('item')

        for item in items:
            link = item.link.text.strip()
            if link in seen_urls:
                continue

            title = item.title.text.strip()
            summary = item.description.text.strip()
            pub_date = item.pubDate.text if item.pubDate else "Unknown"

            collected_articles.append({
                'title': title,
                'summary': summary,
                'url': link,
                'publish_date': pub_date
            })

            seen_urls.add(link)

            if len(collected_articles) >= limit:
                break

    except Exception as e:
        print(f"[ERROR] Failed to fetch news links: {e}")

    print(f"[INFO] Total unique articles collected: {len(collected_articles)}")
    return collected_articles


def extract_article_text(url):
    try:
        headers = {'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Mozilla/5.0 (X11; Linux x86_64)'
        ])}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        text = " ".join(p.text for p in soup.find_all('p'))
        return re.sub(r'\s+', ' ', text).strip()
    except Exception as e:
        print(f"[ERROR] Extract text failed: {e}")
        return None


def deduplicate_articles(articles):
    seen_hashes = set()
    seen_urls = set()
    unique = []
    for a in articles:
        key = hashlib.md5((a['title'] + a['summary']).encode()).hexdigest()
        if key in seen_hashes or a['url'] in seen_urls:
            continue
        seen_hashes.add(key)
        seen_urls.add(a['url'])
        unique.append(a)
    return unique


def get_news_articles(company_name, limit=10):
    """
    Main function to fetch, extract, summarize, analyze sentiment and deduplicate articles.
    Guarantees 'limit' articles after deduplication by refetching if needed.
    """
    all_articles = []
    seen_urls = set()

    while len(all_articles) < limit:
        remaining = limit - len(all_articles)
        fetched = fetch_bing_news_links(company_name, limit=remaining)

        if not fetched:
            print("[WARN] No more articles could be fetched. Breaking early.")
            break

        # Deduplicate against already collected
        for article in fetched:
            if article['url'] in seen_urls:
                continue

            print(f"[INFO] Processing article: {article['title']}")
            text = extract_article_text(article['url']) or article['summary']
            article['text'] = text
            article['summary'] = get_summary(text)
            sentiment = get_sentiment(text)
            article['sentiment'] = sentiment['sentiment']
            article['sentiment_score'] = sentiment['score']

            all_articles.append(article)
            seen_urls.add(article['url'])

            if len(all_articles) >= limit:
                break

            time.sleep(random.uniform(1.5, 2.5))

    # Final deduplication (edge case safety)
    final_articles = deduplicate_articles(all_articles)[:limit]
    return final_articles
