# summarizer.py

import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# Auto-download punkt tokenizer if missing
for resource in ['punkt', 'punkt_tab']:
    try:
        nltk.data.find(f'tokenizers/{resource}')
    except LookupError:
        nltk.download(resource)
        
def get_summary(text, sentence_count=3):
    """
    Generates an extractive summary using LexRank from sumy.

    Args:
        text (str): Full article text.
        sentence_count (int): Number of sentences to include in summary.

    Returns:
        str: Summary string.
    """
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary_sentences = summarizer(parser.document, sentence_count)

        summary_text = " ".join(str(sentence) for sentence in summary_sentences)
        return summary_text.strip()

    except Exception as e:
        print(f"[ERROR] Summary generation failed: {e}")
        return text[:300]  # fallback: just return first 300 characters
