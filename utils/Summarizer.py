import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import os

'''
# NLTK Setup (Safe for Docker)
NLTK_DATA_DIR = os.path.join(os.path.dirname(__file__), "nltk_data")
nltk.data.path.append(NLTK_DATA_DIR)
'''

# Ensure tokenizer downloaded
nltk.download("punkt", quiet=True)

def get_summary(text, sentence_count=3):
    """
    Generates an extractive summary using LexRank.
    """
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary_sentences = summarizer(parser.document, sentence_count)
        summary_text = " ".join(str(sentence) for sentence in summary_sentences)
        return summary_text.strip()
    except Exception as e:
        print(f"[ERROR] Summary generation failed: {e}")
        return text[:300]
