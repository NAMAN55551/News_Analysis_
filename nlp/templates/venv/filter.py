import json
import re
import nltk
import spacy

nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words("english"))
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    if not text:
        return ""
    # Remove URLs, HTML tags, emojis
    text = re.sub(r"http\S+|www\S+|<.*?>|[^a-zA-Z0-9\s]", " ", text)
    text = text.lower()
    
    # Tokenize & remove stopwords
    tokens = [w for w in word_tokenize(text) if w not in stop_words]
    
    # Lemmatize
    doc = nlp(" ".join(tokens))
    lemmas = [token.lemma_ for token in doc]
    return " ".join(lemmas)


with open("/home/naman/Desktop/nlp/all_news.json", "r", encoding="utf-8") as f:
    all_news = json.load(f)

for category, articles in all_news.items():
    for article in articles:
        text = " ".join(filter(None, [article.get("title"), article.get("description"), article.get("content")]))
        article["preprocessed_text"] = preprocess_text(text)



from transformers import pipeline

# Use pre-trained sentiment analysis model
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

for category, articles in all_news.items():
    for article in articles:
        text = article["preprocessed_text"]
        if text:
            result = sentiment_model(text[:512])[0]  # Truncate long text
            article["sentiment"] = result["label"]
            article["sentiment_score"] = result["score"]
        else:
            article["sentiment"] = "NEUTRAL"
            article["sentiment_score"] = 0.0


for category, articles in all_news.items():
    for article in articles:
        text = article["preprocessed_text"]
        doc = nlp(text)
        entities = {"PERSON": [], "ORG": [], "GPE": []}
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)
        article["entities"] = entities


with open("all_news_processed.json", "w", encoding="utf-8") as f:
    json.dump(all_news, f, ensure_ascii=False, indent=4)

print("Processed data saved to all_news_processed.json")