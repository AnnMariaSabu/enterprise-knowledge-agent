import ollama

import config
from rag import NO_ANSWER, search

MAX_STEPS = 4

AGENT_PROMPT = f"""You are Acme Corp's policy assistant.
You have a tool called search_documents that searches the company policies.

Rules:
1. ALWAYS use search_documents before answering a policy question.
2. If the question has more than one topic, search ONCE FOR EACH topic.
3. Answer ONLY using what the searches returned.
4. ONLY if the searches found NOTHING useful for the whole question, reply exactly:
{NO_ANSWER}
   Never add that sentence to an answer that already contains information.
5. Answer in one to three full sentences."""

NO_ANSWER_PHRASES = [
    "i don't know",
    "i do not know",
    "not specified",
    "not mentioned",
    "no information",
    "not found in",
    "does not contain",
    "doesn't contain",
    "not available in",
    "cannot find",
    "can't find",
    "don't have information",
    "do not have information",
    "did not provide",
    "does not provide",
    "doesn't provide",
    "no details",
]

search_tool = {
    "type": "function",
    "function": {
        "name": "search_documents",
        "description": "Search Acme Corp's HR, IT and travel policy documents.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A short search about ONE topic, e.g. 'sick leave days'",
                },
            },
            "required": ["query"],
        },
    },
}


def sounds_like_no_answer(text):
    lowered = text.lower()
    for phrase in NO_ANSWER_PHRASES:
        if phrase in lowered:
            return True
    return False


def search_documents(query, role, passages):
    chunks = search(query, role)

    result_text = ""
    for chunk in chunks:
        close_meaning = chunk["distance"] <= config.MAX_DISTANCE
        strong_keywords = chunk.get("keyword_score", 0) >= config.MIN_KEYWORD_SCORE
        if close_meaning or strong_keywords:
            result_text = result_text + f"(source: {chunk['source']})\n{chunk['text']}\n\n"
            passage = {"source": chunk["source"], "text": chunk["text"]}
            if passage not in passages:
                passages.append(passage)

    if not result_text:
        return "No relevant information found."
    return result_text


def run_agent(question, role):
    messages = [
        {"role": "system", "content": AGENT_PROMPT},
        {"role": "user", "content": question},
    ]
    searches = []
    passages = []

    for step in range(MAX_STEPS):
        response = ollama.chat(
            model=config.CHAT_MODEL,
            messages=messages,
            tools=[search_tool],
            options={"temperature": 0},
        )
        messages.append(response.message)

        if not response.message.tool_calls:
            answer_text = response.message.content
            break

        for call in response.message.tool_calls:
            if call.function.name != "search_documents":
                result = "Unknown tool."
            else:
                query = str(call.function.arguments.get("query", ""))
                searches.append(query)
                result = search_documents(query, role, passages)
            messages.append({"role": "tool", "content": result})
    else:
        messages.append({"role": "user", "content": "Please give your final answer now."})
        response = ollama.chat(
            model=config.CHAT_MODEL,
            messages=messages,
            options={"temperature": 0},
        )
        answer_text = response.message.content

    cleaned = answer_text.replace(NO_ANSWER, "").strip()

    if not passages or not cleaned or sounds_like_no_answer(cleaned):
        return {"answer": NO_ANSWER, "searches": searches, "passages": []}

    return {"answer": cleaned, "searches": searches, "passages": passages}


if __name__ == "__main__":
    role = input("Your role (Employee / HR / IT / Admin): ").strip()
    print(f"Acme Policy Agent ({role}). Type 'quit' to stop.")

    while True:
        question = input("\nAsk: ").strip()

        if question.lower() in ("quit", "q", "exit"):
            break
        if not question:
            continue

        result = run_agent(question, role)
        for i, query in enumerate(result["searches"], start=1):
            print(f"  🔍 Search {i}: {query}")
        print("\nAnswer:", result["answer"])