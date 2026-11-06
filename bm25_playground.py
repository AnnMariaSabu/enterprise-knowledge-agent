import re

from rank_bm25 import BM25Okapi

from permissions import search_filter
from rag import get_collection


STOPWORDS = {
    "a", "an", "the", "is", "are", "am", "was", "be", "of", "to", "in", "on",
    "at", "for", "and", "or", "with", "about", "do", "does", "did", "i", "my",
    "me", "you", "your", "we", "what", "who", "which", "when", "where", "how",
    "why", "can", "could", "should", "would", "will", "this", "that", "there",
    "many", "much", "get",
}


def tokenize(text):
    words = re.findall(r"\w+", text.lower())
    kept = []
    for word in words:
        if word not in STOPWORDS:
            kept.append(word)
    return kept


collection = get_collection()
data = collection.get(where=search_filter("Employee"))

texts = data["documents"]
sources = []
tokenized = []
for text, meta in zip(texts, data["metadatas"]):
    sources.append(meta["source"])
    tokenized.append(tokenize(text))

bm25 = BM25Okapi(tokenized)

for query in ["holiday days December", "IT helpdesk extension", "Who is the CEO of Acme Corp"]:
    scores = bm25.get_scores(tokenize(query))
    ranked = sorted(zip(scores, sources, texts), reverse=True)

    print()
    print("QUERY:", query)
    for score, source, text in ranked[:3]:
        print(f"  {round(score, 2):>5}  {source:<30} {text[:60]}...")