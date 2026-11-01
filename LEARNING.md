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