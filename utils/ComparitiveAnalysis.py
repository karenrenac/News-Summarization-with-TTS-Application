from collections import Counter
import statistics
import re
import itertools
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import os
#model = SentenceTransformer('all-MiniLM-L6-v2')

model_path = os.path.join(os.path.dirname(__file__), "..", "hf_model")
model = SentenceTransformer(model_path)

def extract_topics(text, top_n=3):
    """
    Extract key topics from article titles using simple NLP logic.
    """
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    stopwords = {
        "about", "from", "with", "this", "that", "which", "have", "been", "they",
        "will", "their", "into", "more", "news"
    }
    filtered = [w for w in words if w not in stopwords]
    return list(dict(Counter(filtered).most_common(top_n)).keys())


def sentiment_distribution(articles):
    sentiments = [a['sentiment'] for a in articles]
    scores = [a['sentiment_score'] for a in articles if isinstance(a['sentiment_score'], (int, float))]
    return Counter(sentiments), round(statistics.mean(scores), 3) if scores else 0.0


def topic_overlap(articles):
    all_topics = [set(a.get('topics', [])) for a in articles]
    flat_topics = list(itertools.chain.from_iterable(all_topics))
    common_topics = [item for item, count in Counter(flat_topics).items() if count > 1]

    topic_dict = {
        "Common Topics": list(set(common_topics))
    }

    for i, topics in enumerate(all_topics):
        unique = list(topics - set(common_topics))
        topic_dict[f"Unique Topics in Article {i+1}"] = unique

    return topic_dict


def generate_impact_narrative(summary1, summary2, similarity_score):
    if similarity_score > 0.85:
        return "Both articles delve into closely connected developments, emphasizing overlapping themes in the company’s recent news cycle."
    elif similarity_score > 0.75:
        return "The two articles share considerable thematic overlap, suggesting a broader narrative link in coverage."
    elif similarity_score > 0.65:
        return "The articles discuss related but distinct subjects, offering complementary insights into the company's current standing."
    elif similarity_score > 0.55:
        return "The articles cover separate areas of interest, yet loosely connect under the broader corporate or product landscape."
    else:
        return "These articles explore different aspects altogether, reflecting a diverse range of news angles around the company."


def generate_coverage_comparisons(articles):
    comparisons = []
    if len(articles) < 2:
        return comparisons

    article_pairs = list(itertools.combinations(enumerate(articles), 2))

    summaries = [article["summary"] for article in articles]
    embeddings = model.encode(summaries)

    for (i1, a1), (i2, a2) in article_pairs:
        sim_score = cosine_similarity([embeddings[i1]], [embeddings[i2]])[0][0]
        comparison = (
            f"Article {i1 + 1} discusses: '{a1['summary']}'\n"
            f"Article {i2 + 1} discusses: '{a2['summary']}'"
        )
        impact = generate_impact_narrative(a1['summary'], a2['summary'], sim_score)

        comparisons.append({
            "Comparison": comparison,
            "Impact": impact
        })

    return comparisons


def generate_sentiment_summary(articles, company_name="The company"):
    sentiment_dist, _ = sentiment_distribution(articles)
    pos = sentiment_dist.get("Positive", 0)
    neg = sentiment_dist.get("Negative", 0)
    neutral = sentiment_dist.get("Neutral", 0)

    if pos > max(neg, neutral):
        return f"{company_name}'s news coverage is mostly positive, highlighting strong performance and positive developments."
    elif neg > max(pos, neutral):
        return f"{company_name} has received mostly critical coverage, pointing to performance issues or market concerns."
    elif neutral > max(pos, neg):
        return f"{company_name}'s media presence is largely neutral, focused on factual and balanced reporting."
    else:
        return f"{company_name}'s coverage appears mixed, presenting a range of contrasting perspectives."


def generate_structured_analysis(company, articles):
    for article in articles:
        article['topics'] = extract_topics(article['title'])

    sentiment_dist, avg_score = sentiment_distribution(articles)

    report = {
        "Company": company,
        "Articles": [
            {
                "Title": a['title'],
                "Summary": a['summary'],
                "Sentiment": a['sentiment'],
                "Topics": a['topics']
            }
            for a in articles
        ],
        "Comparative Sentiment Score": {
            "Sentiment Distribution": dict(sentiment_dist),
            "Coverage Differences": generate_coverage_comparisons(articles),
            "Topic Overlap": topic_overlap(articles)
        },
        "Final Sentiment Analysis": generate_sentiment_summary(articles, company)
    }

    return report
