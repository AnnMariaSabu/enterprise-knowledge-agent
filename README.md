# 🤖 Enterprise Knowledge Agent

A **private AI assistant** that answers employee questions using the company's own
documents (HR, IT and travel policies). It shows **where each answer came from**, and
says **"I don't know"** when the answer isn't in the documents.

Everything runs **locally on a laptop**: free, and company documents never leave the computer.

> 🙋 *"How many sick days do I get, and what is the hotel limit abroad?"*
> 🤖 *"You are entitled to 10 days of paid sick leave per year. For international trips, the hotel limit is $220 per night."*
> 📎 Sources: `hr/hr_policy.txt`, `travel/travel_policy.txt`

---

## ✨ Features

- 💬 **Chat website** (Streamlit) with answers, **sources** and the exact **passages** used
- 🔍 **RAG** (Retrieval-Augmented Generation): answers come only from company documents
- 🛡️ **"I don't know"** instead of made-up answers (safety checks in code, not only in the prompt)
- 🧠 **Memory**: follow-up questions work ("Can I carry **them** over?")
- 🤖 **Agent**: the AI decides what and how many times to search, so multi-topic questions work
- 🔒 **Role-based permissions**: Employee / HR / IT / Admin. Restricted documents are filtered
  out **in the database**, so the AI never sees them
- 🔀 **Hybrid search**: meaning search (embeddings) + keyword search (BM25)
- 📤 **Upload** new documents from the website; they are searchable immediately
- 🔁 **Smart ingestion**: only new, changed or deleted files are reprocessed
- 📏 **Automatic evaluation** on 40 test questions with known answers

---

## ⚙️ How it works

**Stage 1: Prepare the documents** (`python ingest.py`)

1. **Read** `.txt`, `.pdf` and `.docx` files
2. **Chunk** them into pieces of 80 words with a 20-word overlap
3. **Embed** each chunk into 768 numbers that capture its meaning (`nomic-embed-text`)
4. **Store** chunks, embeddings and metadata (source, department, access level) in **ChromaDB**
5. A **SHA-256 fingerprint** of each file detects new, changed and deleted files

**Stage 2: Answer a question**

1. **Rewrite** follow-up questions using the chat history
2. The **agent** (`llama3.2`) calls a `search_documents` tool, once per topic
3. Each search combines **meaning** and **keyword** results (Reciprocal Rank Fusion),
   filtered by the user's **role**
4. Only chunks that are close enough are kept; if none are, the answer is **"I don't know"**
5. The LLM writes the answer at temperature 0, and the sources come from the chunks' metadata

```mermaid
flowchart TB
  U["Employee in browser"] --> UI["app.py (Streamlit)"]
  UI -->|"question, role, history"| RW["rewrite_question (memory)"]
  RW --> AG["agent.py (llama3.2 + search tool)"]
  AG -->|"search_documents(query)"| S["rag.py: hybrid search"]
  S --> P["permissions.py: role filter"]
  S -->|"meaning"| DB[("ChromaDB")]
  S -->|"keywords"| BM["BM25"]
  AG -->|"answer + searches + sources"| UI
  UP["Upload button"] --> ING["ingest.py"]
  ING --> DB
```

---

## 🧰 Tech stack

| Part | Tool |
|---|---|
| Language | Python 3.12 |
| LLM (answers) | Ollama + `llama3.2` (3B) |
| Embeddings | Ollama + `nomic-embed-text` |
| Vector database | ChromaDB |
| Reading files | `pypdf`, `python-docx` |
| Keyword search | `rank-bm25` |
| Chat website | Streamlit |

All free and running locally.

---

## 📁 Project structure

| File | What it does |
|---|---|
| `config.py` | all settings in one place |
| `loaders.py` | reads `.txt`, `.pdf` and `.docx` files |
| `chunker.py` | splits text into overlapping word chunks |
| `ingest.py` | loads all documents into ChromaDB (only what changed) |
| `rag.py` | search (meaning + hybrid), question rewriting, answers |
| `permissions.py` | role rules: who may see which documents |
| `agent.py` | the tool-using agent |
| `app.py` | the Streamlit chat website |
| `evaluate.py` | runs the test questions and prints the scores |
| `data/documents/` | sample "Acme Corp" policies (fake data) |
| `data/test_questions.json` | 40 test questions with known answers |
| `*_playground.py` | small experiments I used while learning |

---

## 🚀 Setup (Windows)

1. Install [Python 3.12](https://www.python.org/) and [Ollama](https://ollama.com/download)
2. Download the AI models:
   ```bash
   ollama pull llama3.2
   ollama pull nomic-embed-text
   ```
3. Create a virtual environment and install the libraries:
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
4. Load the documents into the database:
   ```bash
   python ingest.py
   ```
5. Start the chat website:
   ```bash
   streamlit run app.py
   ```
   It opens at `http://localhost:8501`.

Other commands:
- `python agent.py`: chat with the agent in the terminal
- `python evaluate.py`: run the 40 test questions

---

## 🔒 Permissions

| Role | Can see |
|---|---|
| Employee | public documents only |
| HR | public + all HR documents (including salary bands) |
| IT | public + all IT documents (including the server admin guide) |
| Admin | everything |

Restricted chunks are filtered **in the database query**, before the AI sees anything, so a
question like *"Ignore your rules, I am the HR director..."* cannot reveal them.

> Note: the role is chosen from a dropdown, as a stand-in for login. In a real company it
> would come from company login (SSO); the permission logic would stay the same.

---

## 📊 Test results

40 test questions: 32 answerable, 5 not covered by the documents, and permission tests
(Employee must be blocked, HR/IT must be allowed). Run with `python evaluate.py`.

| Run | Change | Answers correct | "I don't know" correct | Overall |
|---|---|---|---|---|
| Baseline | meaning search only | 31/32 | 7/8 | **38/40 (95%)** |
| + hybrid search | meaning + keywords (BM25 + RRF) | 32/32 | 5/8 | 37/40 (92%) |
| + better "no answer" detection | final version | **32/32** | **7/8** | **39/40 (98%)** |

**What I found:**
- Hybrid search fixed a question that used different words than the document
  ("holiday" vs "annual leave"): the exact word "December" matched.
- It also let more borderline text through, so the AI said "no information" in new
  wordings. Detecting those wordings fixed it.
- A prompt rule I tried ("don't stretch similar facts") caused a regression, so I removed it.

---

## ⚠️ Known limitations

- The small model (3B) sometimes stretches a related fact: asked about **admin** passwords,
  an Employee gets the **normal** password rule. No restricted data leaks.
- "No answer" detection uses a list of phrases, which could miss new wordings.
- The role dropdown is not real authentication.
- Tested with a small set of sample documents.

## 🔮 Future improvements

- A bigger model on a company server, or a cloud AI API
- A second AI check that verifies the answer matches the question
- Company login (SSO), and an admin area to manage documents
- pgvector or Qdrant instead of ChromaDB for large document sets
- Connectors to SharePoint, Confluence or Google Drive
- Testing other chunk sizes

---

## 🎓 What I learned

I built this project step by step as my first project, writing and testing every part myself.
Along the way I learned Python, Git, embeddings, vector databases, RAG, prompt engineering,
tool-calling agents, role-based access control, hybrid search, and how to measure and
improve an AI system with real test results.