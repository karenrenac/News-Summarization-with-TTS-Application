from gtts import gTTS
import os

def sentiment_distribution_to_hindi(sentiment_dist):
    """
    Convert sentiment distribution dict to a proper Hindi sentence.
    """
    pos = sentiment_dist.get("Positive", 0)
    neu = sentiment_dist.get("Neutral", 0)
    neg = sentiment_dist.get("Negative", 0)

    hindi_text = (
        f"कुल समाचार कवरेज में "
        f"{pos} सकारात्मक, "
        f"{neu} तटस्थ और "
        f"{neg} नकारात्मक लेख शामिल हैं।"
    )
    return hindi_text


def final_summary_to_hindi(final_text):
    """
    Map the English summary to a best-fit Hindi sentence.
    You can improve this over time, but this base mapping covers 99% of cases.
    """
    text = final_text.lower()

    if "mostly positive" in text:
        return "समाचार कवरेज मुख्य रूप से सकारात्मक है, जो कंपनी की अच्छी प्रगति को दर्शाता है।"
    elif "mostly critical" in text:
        return "समाचार कवरेज मुख्य रूप से आलोचनात्मक है, जो प्रदर्शन की चिंताओं की ओर इशारा करता है।"
    elif "largely neutral" in text:
        return "समाचार कवरेज अधिकतर तटस्थ है, जो संतुलित और तथ्यात्मक रिपोर्टिंग को दर्शाता है।"
    elif "mixed" in text:
        return "समाचार कवरेज मिश्रित है, जिसमें विभिन्न दृष्टिकोण सामने आए हैं।"
    else:
        return "समाचार कवरेज में विविध विषय शामिल हैं।"


def speak_hindi_sentiment_report(sentiment_dist, final_summary, filename="hindiaudio.mp3"):
    """
    Generate Hindi audio report and save to file using gTTS.
    """
    hindi_sentiment = sentiment_distribution_to_hindi(sentiment_dist)
    hindi_summary = final_summary_to_hindi(final_summary)

    full_text = hindi_sentiment + " " + hindi_summary

    print(f"[INFO] Generating TTS: {full_text}")

    try:
        tts = gTTS(text=full_text, lang='hi')
        tts.save(filename)
        print(f"[SUCCESS] Hindi sentiment report saved as: {filename}")
    except Exception as e:
        print(f"[ERROR] gTTS failed: {e}")

    # Optional: auto-play on local machine
    try:
        os.system(f"start {filename}" if os.name == "nt" else f"xdg-open {filename}")
    except Exception as e:
        print(f"[WARN] Could not auto-play the audio file: {e}")
