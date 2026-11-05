import ollama

import config
from rag import NO_ANSWER, retrieve

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


def search_documents(query, role, passages):
    chunks = retrieve(query, role)

    result_text = ""
    for chunk in chunks:
        
        if chunk["distance"] <= config.MAX_DISTANCE:
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

    answer_text = answer_text.strip()


    if not passages or answer_text.startswith("I don't know"):
        return {"answer": NO_ANSWER, "searches": searches, "passages": []}

    if NO_ANSWER in answer_text:
        answer_text = answer_text.replace(NO_ANSWER, "").strip()

    return {"answer": answer_text, "searches": searches, "passages": passages}


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