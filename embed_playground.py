import math
import ollama
import config

def cosine_similarity(a, b):
    dot = 0
    length_a = 0
    length_b = 0
    for x, y in zip(a, b):
        dot = dot + x * y
        length_a = length_a + x * x
        length_b = length_b + y * y
    return dot / (math.sqrt(length_a) * math.sqrt(length_b))


question = "search_query: How many sick days do I get?"
sentences = [
    "search_document: Employees receive 10 days of paid sick leave per year.",
    "search_document: Staff who are ill can take time off with pay.",
    "search_document: Passwords must be changed every 90 days.",
    "search_document: The hotel limit is 150 US dollars per night.",
]

response = ollama.embed(model=config.EMBED_MODEL, input=[question] + sentences)
vectors = response["embeddings"]
question_vector = vectors[0]

for sentence, vector in zip(sentences, vectors[1:]):
    score = cosine_similarity(question_vector, vector)
    print(round(score, 3), "-", sentence)