import chromadb
import ollama

import config


NO_ANSWER = "I don't know based on the company documents."

SYSTEM_PROMPT = f"""You are Acme Corp's policy assistant. You answer employee questions.

Rules:
1. Use ONLY the information in the context below.
2. Answer in one or two full sentences.
3. At the end of your answer, add the numbers of the context pieces you used, like [3].
4. If the answer is not in the context, reply exactly:
{NO_ANSWER}

Example of a good answer:
The office closes at 6 PM on Fridays. [2]"""


def get_collection():
    client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    return client.get_collection(config.COLLECTION_NAME)


def retrieve(question, k=config.TOP_K):
    collection = get_collection()

    response = ollama.embed(model=config.EMBED_MODEL, input="search_query: " + question)
    question_vector = response["embeddings"][0]

    results = collection.query(query_embeddings=[question_vector], n_results=k)

    chunks = []
    for text, meta, distance in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        chunks.append({"text": text, "source": meta["source"], "distance": distance})
    return chunks


def build_messages(question, chunks):
    context = ""
    for i, chunk in enumerate(chunks, start=1):
        context = context + f"[{i}] (source: {chunk['source']})\n{chunk['text']}\n\n"

    user_message = f"Context:\n{context}Question: {question}"

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]


def answer(question):
    chunks = retrieve(question)

    if chunks[0]["distance"] > config.MAX_DISTANCE:
        return {"answer": NO_ANSWER, "sources": []}

    messages = build_messages(question, chunks)

    response = ollama.chat(
        model=config.CHAT_MODEL,
        messages=messages,
        options={"temperature": 0},
    )
    answer_text = response["message"]["content"]

    if answer_text.startswith("I don't know"):
        return {"answer": NO_ANSWER, "sources": []}

    sources = []
    for chunk in chunks:
        if chunk["source"] not in sources:
            sources.append(chunk["source"])

    return {"answer": answer_text, "sources": sources}


if __name__ == "__main__":
    print("Acme Policy Assistant. Type 'quit' to stop.")

    while True:
        question = input("\nAsk: ").strip()

        if question.lower() in ("quit", "q", "exit"):
            break
        if not question:
            continue

        result = answer(question)
        print("\nAnswer:", result["answer"])
        if result["sources"]:
            print("Sources:", ", ".join(result["sources"]))