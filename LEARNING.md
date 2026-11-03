# My Learning Journal

## Phase 1 - Project setup (1 November 2026)

### What I built
- Set up a Python project with its own virtual environment (venv) and Git.
- Wrote config.py to keep all project settings in one place.
- Created 7 test documents for "Acme Corp" (HR, IT and travel):
  .txt, .docx and .pdf files, including 2 restricted (secret) files.
- Wrote Python scripts to create a Word file and a PDF file.
- Wrote check_setup.py: it finds all documents and gets a reply
  from the local AI (llama3.2) through Ollama.

### New words I learned
- **Terminal:** a window where I type commands instead of clicking.
- **venv (virtual environment):** a separate toolbox for each project,
  so each project keeps its own libraries and they don't clash.
- **pip:** Python's app store. It installs libraries.
- **Library:** ready-made code written by someone else that I can use
  (for example chromadb, streamlit, ollama).
- **Dependency:** a library that another library needs to work.
  pip installs these automatically.
- **requirements.txt:** the shopping list of all libraries my project needs.
  Anyone can install them with: pip install -r requirements.txt
- **Git:** saves snapshots of my project so I can go back if something breaks.
- **Git commit:** a save point with a message.
  - git add = choose what to save (put it in the box)
  - git commit = create the save point (seal the box with a label)
- **.gitignore:** a list of files Git must never save,
  like .venv (huge, can be rebuilt) and chroma_db.
- **config.py:** keeps all project settings in one place
  (model names, folder paths, chunk size). Change once, every file uses it.
- **import:** lets one Python file use code from another file or library.
- **String vs integer:** "500" (with quotes) is text, 500 is a number.
- **List [ ]:** an ordered collection of items. Can be changed later.
- **Tuple ( ):** like a list, but cannot be changed once created.
- **Dictionary { }:** key-value pairs, like a form with labelled boxes.
  Example: {"role": "user", "content": "Hello"}
- **Set { }:** a collection with no duplicates. Good for checking
  "is this item in the group?"
- **for loop:** repeats the same code once for each item in a list.
  Example: in make_docx.py the loop ran 5 times, once per section.
- **if statement:** runs code only when a condition is true.
- **Path:** a smart way to write file and folder locations.
  / joins folder names, and it works on Windows and Mac.
- **Git vs GitHub:** Git saves snapshots on my laptop (offline).
  GitHub is a website that stores my project online.
  Code only goes to GitHub when I run git push.

### Commands I can use now
- python -m venv .venv          -> create a virtual environment
- .venv\Scripts\Activate.ps1    -> turn it on
- pip install <name>            -> install a library
- pip freeze > requirements.txt -> save my library list
- git init / git status / git add . / git commit -m "..." / git log --oneline
- python file.py                -> run a Python file

### Mistakes I made and what I learned
- I typed file content into the terminal and got errors.
  Lesson: the terminal is for commands; file content goes in the editor.

### What confused me
- Nothing big yet.

### What I'm proud of
- I started my first project journey, and my own Python code
  talked to an AI running on my laptop!





  - **Embedding:** a list of 768 numbers that represents the meaning of text.
  Similar meaning = similar numbers ("GPS for meaning").
- **Cosine similarity:** a score for how much two embeddings point the same
  way. 1 = same meaning, 0 = unrelated. The ranking matters more than the
  exact number.
- **Experiment:** "ill / time off with pay" scored high for "sick days"
  with no shared words, so the model understands meaning, not just words.



  
---

## Phase 2 - Prepare the documents (2-3 November 2026)

### What I built
- **loaders.py**: reads text from .txt, .pdf and .docx files.
  load_text() looks at the file ending and picks the right reader.
- **chunker.py**: cuts text into overlapping chunks of 80 words
  (20 words overlap), so no word is cut in half.
- **embed_playground.py**: experiments with embeddings and my own
  cosine similarity function.
- **chroma_playground.py**: practised storing, searching, filtering
  and deleting in ChromaDB.
- **ingest.py**: one command (python ingest.py) loads all 7 documents
  (19 chunks) into ChromaDB. It only redoes what changed:
  - unchanged file -> skipped
  - changed file -> old chunks deleted, new chunks saved
  - new file -> added
  - deleted file -> its chunks removed
- **peek_db.py**: shows every chunk id and its labels in the database.

### New words I learned
- **Chunk:** a small piece of a document (like an index card).
  Small pieces make search more precise.
- **Overlap:** each chunk repeats the end of the previous one,
  so a fact cut at the edge still appears whole somewhere.
- **Embedding:** a list of 768 numbers that represents the meaning
  of text. Similar meaning = similar numbers ("GPS for meaning").
- **Vector:** a list of numbers. An embedding is a vector.
- **Cosine similarity:** a score for how much two vectors point the
  same way. 1 = same meaning, 0 = unrelated.
- **Distance:** what ChromaDB shows. Distance = 1 - similarity.
  Smaller distance = better match.
- **Vector database (ChromaDB):** stores chunks with their embeddings
  and labels, and quickly finds the ones closest to a question.
- **Collection:** a named group of items in ChromaDB (like a drawer).
- **Metadata:** labels on each chunk (source, department, access,
  chunk_index, file_hash). Used for sources and permissions.
- **Upsert:** update if the id exists, insert if it doesn't.
- **Idempotent:** running something twice gives the same result as
  running it once (no duplicates).
- **Hash (fingerprint):** a code made from a file's content. Same
  content = same hash. Change one letter = completely different hash.
  Used to spot changed files.
- **Refactoring:** reorganising code without changing what it does
  (I moved the ingest code into run_ingest() so other files can use it).
- **Infinite loop:** a loop that never stops. Stop it with Ctrl + C.
- **Traceback:** Python's error report. Read it from the bottom up:
  the last line says WHAT went wrong, the lines above say WHERE.

### Python I learned
- **def / return:** create a reusable function and give back a result.
- **if __name__ == "__main__":** only run this code when I start the
  file directly, not when another file imports it.
- **Slicing:** text[:200], words[start:start + size], vectors[1:]
- **.append()** adds to a list, **.add()** adds to a set.
- **"\n".join(list)** glues items together. **.split()** does the opposite.
- **if / elif / else:** choose between several options. == compares.
- **raise ValueError("...")**: stop with a clear error message on purpose.
- **f-strings:** f"Chunk {i}" puts values inside text.
- **while loop:** repeat as long as a condition is true.
- **break:** leave the loop completely. **continue:** skip to the next round.
- **enumerate:** gives a counter and the item: for i, chunk in enumerate(chunks)
- **zip:** walks through two or more lists side by side.
- **Dictionary .get():** returns None instead of crashing if the key is missing.
- **set():** an empty set ({} would be an empty dictionary).
- **in / not in:** check if something is inside a list, set or tuple.
- Importing from my own files: from loaders import load_text

### Experiments and what I found
- "Staff who are ill can take time off with pay" matched
  "How many sick days do I get?" with NO shared words.
  The model understands meaning, not just words.
- Unrelated sentences still scored about 0.5, not 0.
  The ranking matters more than the exact number.
- Removing the search_query / search_document labels lowered all scores
  but kept the same ranking. One small test isn't proof; I'll measure
  properly in Phase 6.
- ChromaDB's distance (0.191) was exactly 1 - my own similarity (0.809).
  So I understand what happens inside the database.
- A database search always returns the closest match, even if it's a
  bad one. I'll need an "I don't know" check in Phase 3.

### Mistakes I made and what I learned
- Ran a file before saving it. Lesson: check for the white dot on the
  tab and press Ctrl + S before running.
- Deleted the test part of a file by accident, so nothing printed.
  Lesson: "no output and no error" means nothing asked Python to print.
- Changed the code but forgot to update config.py (got 1 big chunk).
  Lesson: settings in config.py affect the whole project.
- Got stuck in "git log" showing (END). Lesson: press q to quit.
- Some words looked joined in the terminal ("sickleave"), but the file
  was fine. Lesson: check the source file before changing it.

### What confused me
- The sliding window logic in split_text at first. Adding a print inside
  the loop and watching it run helped me understand it.

### What I'm proud of
- One command now loads all my documents into a vector database, and it
  is smart enough to notice new, changed and deleted files.
  - **Temperature:** how the AI picks each next word. 0 = always the most
  likely word (same answer every time, good for facts). 1 = more random
  (different answers, sometimes wrong). My project uses 0.