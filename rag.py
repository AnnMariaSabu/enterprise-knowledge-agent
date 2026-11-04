import chromadb
import ollama

import config
from permissions import search_filter


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

REWRITE_PROMPT = """You help a search engine. Look at the conversation and the user's last question.

- If the last question depends on the conversation (for example it uses words like
  "it", "them", "ones", "that" or "and for..."), rewrite it so it makes sense on its own.
- If the last question is already complete, or is about a NEW topic,
  return it EXACTLY as it is. Never change its topic.

Reply with ONLY the question, nothing else.

Example 1:
Conversation: the user asked about annual leave days.
Last question: Can I carry them over?
Reply: Can I carry over unused annual leave days?

Example 2:
Conversation: the user asked about passwords.
Last question: What is the capital of France?
Reply: What is the capital of France?"""


def get_collection():
    client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    return client.get_collection(config.COLLECTION_NAME)


def retrieve(question, role, k=config.TOP_K):
    collection = get_collection()

    response = ollama.embed(model=config.EMBED_MODEL, input="search_query: " + question)
    question_vector = response["embeddings"][0]

    results = collection.query(
        query_embeddings=[question_vector],
        n_results=k,
        where=search_filter(role),
    )

    chunks = []
    for text, meta, distance in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        chunks.append({"text": text, "source": meta["source"], "distance": distance})
    return chunks


def rewrite_question(question, history):
    if not history:
        return question

    conversation = ""
    for message in history[-4:]:
        conversation = conversation + f"{message['role']}: {message['content']}\n"

    messages = [
        {"role": "system", "content": REWRITE_PROMPT},
        {"role": "user", "content": f"Conversation:\n{conversation}\nLast question: {question}"},
    ]
    response = ollama.chat(
        model=config.CHAT_MODEL,
        messages=messages,
        options={"temperature": 0},
    )
    return response["message"]["content"].strip()


def build_messages(question, chunks):
    context = ""
    for i, chunk in enumerate(chunks, start=1):
        context = context + f"[{i}] (source: {chunk['source']})\n{chunk['text']}\n\n"

    user_message = f"Context:\n{context}Question: {question}"

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]


def answer(question, role, history=None):
    search_question = rewrite_question(question, history)
    chunks = retrieve(search_question, role)

    if not chunks or chunks[0]["distance"] > config.MAX_DISTANCE:
        return {"answer": NO_ANSWER, "sources": [], "passages": [],
                "search_question": search_question}

    messages = build_messages(search_question, chunks)

    response = ollama.chat(
        model=config.CHAT_MODEL,
        messages=messages,
        options={"temperature": 0},
    )
    answer_text = response["message"]["content"]

    if answer_text.startswith("I don't know"):
        return {"answer": NO_ANSWER, "sources": [], "passages": [],
                "search_question": search_question}

    sources = []
    passages = []
    for chunk in chunks:
        if chunk["source"] not in sources:
            sources.append(chunk["source"])
        passages.append({"source": chunk["source"], "text": chunk["text"]})

    return {"answer": answer_text, "sources": sources, "passages": passages,
            "search_question": search_question}


if __name__ == "__main__":
    role = input("Your role (Employee / HR / IT / Admin): ").strip()
    print(f"Acme Policy Assistant ({role}). Type 'quit' to stop.")

    while True:
        question = input("\nAsk: ").strip()

        if question.lower() in ("quit", "q", "exit"):
            break
        if not question:
            continue

        result = answer(question, role)
        print("\nAnswer:", result["answer"])
        if result["sources"]:
            print("Sources:", ", ".join(result["sources"]))