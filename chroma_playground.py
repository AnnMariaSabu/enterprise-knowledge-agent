import chromadb
import ollama
import config

client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
collection = client.get_or_create_collection(
    name="playground",
    metadata={"hnsw:space": "cosine"},
)

texts = [
    "Employees receive 10 days of paid sick leave per year.",
    "Passwords must be changed every 90 days.",
    "The hotel limit is 150 US dollars per night.",
]

labelled = []
for t in texts:
    labelled.append("search_document: " + t)

response = ollama.embed(model=config.EMBED_MODEL, input=labelled)

collection.upsert(
    ids=["hr-1", "it-1", "travel-1"],
    documents=texts,
    embeddings=response["embeddings"],
    metadatas=[
        {"department": "hr"},
        {"department": "it"},
        {"department": "travel"},
    ],
)

print("Items in the collection:", collection.count())
question = "How many sick days do I get?"
q_response = ollama.embed(model=config.EMBED_MODEL, input="search_query: " + question)
question_vector = q_response["embeddings"][0]

results = collection.query(query_embeddings=[question_vector], n_results=2)

print()
print("Question:", question)
for text, meta, distance in zip(
    results["documents"][0], results["metadatas"][0], results["distances"][0]
):
    print(round(distance, 3), meta["department"], "-", text)

collection.delete(where={"department": "travel"})
print()
print("After deleting travel:", collection.count())