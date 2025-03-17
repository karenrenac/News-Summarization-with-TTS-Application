# news_scraper.py

import requests
from bs4 import BeautifulSoup
import random
import time
import re

# ---------------------------------------------
# Rotating User-Agents to avoid getting blocked
# ---------------------------------------------
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
]

HEADERS = {'User-Agent': random.choice(USER_AGENTS)}

# Template URL for Google News search (non-JS)
GOOGLE_NEWS_URL = "https://www.google.com/search?q={query}&tbm=nws"

# ------------------------------------------------------------------------------
def fetch_google_news_links(company_name, limit=10):
    """
    Fetches top news article links from Google News for a given company.
    
    Parameters:
        company_name (str): Name of the company (e.g., 'Tesla')
        limit (int): Max number of news links to fetch

    Returns:
        list: A list of cleaned, unique article URLs.
    """
    query = f"{company_name} news"
    url = GOOGLE_NEWS_URL.format(query=query.replace(" ", "+"))

    print(f"[INFO] Fetching news for company: {company_name}")
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch news links. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    links = []

    for anchor in soup.find_all('a', href=True):
        href = anchor.get('href')
        
        # Google wraps real URLs like /url?q=https://real-news-site.com
        if "/url?q=" in href:
            cleaned_url = href.split("/url?q=")[1].split("&")[0]
            
            # Filter out garbage links
            if not cleaned_url.startswith("https://www.google.com"):
                links.append(cleaned_url)

        if len(links) >= limit:
            break

    return list(set(links))  # Remove duplicates

# ------------------------------------------------------------------------------
def extract_article_data(url):
    """
    Extracts metadata and content from a news article URL.

    Parameters:
        url (str): The full article URL

    Returns:
        dict: A dictionary with title, summary, publish_date, content, etc.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code != 200:
            print(f"[WARN] Skipping URL {url} — Status Code: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Title extraction
        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else "No Title Found"

        # Attempt to extract publish date from meta tags
        publish_date = None
        for meta in soup.find_all("meta"):
            if 'property' in meta.attrs and meta.attrs['property'] in ['article:published_time', 'og:published_time']:
                publish_date = meta.attrs.get('content', None)

        # Extract article body (all <p> tags)
        paragraphs = soup.find_all('p')
        article_text = " ".join([p.text for p in paragraphs])
        article_text = re.sub(r'\s+', ' ', article_text).strip()

        # Generate a simple summary (first 2–3 sentences)
        sentences = re.split(r'(?<=[.!?]) +', article_text)
        summary = " ".join(sentences[:3]) if len(sentences) >= 3 else article_text[:300]

        return {
            'url': url,
            'title': title,
            'summary': summary,
            'text': article_text,
            'publish_date': publish_date if publish_date else "Unknown"
        }

    except Exception as e:
        print(f"[ERROR] Failed to extract article at {url}: {e}")
        return None

# ------------------------------------------------------------------------------
def get_news_articles(company_name, limit=10):
    """
    Driver function that fetches article URLs and parses content.

    Parameters:
        company_name (str): Company to search for
        limit (int): Number of articles to extract

    Returns:
        list: List of article data dictionaries
    """
    links = fetch_google_news_links(company_name, limit=limit)
    articles = []

    for url in links:
        time.sleep(random.uniform(1.5, 3.5))  # Delay to prevent rate-limiting
        article_data = extract_article_data(url)
        if article_data:
            articles.append(article_data)

    return articles
