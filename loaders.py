from pypdf import PdfReader
from docx import Document
def load_txt(path):
    return path.read_text(encoding="utf-8")

def load_pdf(path):
    reader = PdfReader(path)
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text())
    return "\n".join(pages)

def load_docx(path):
    doc = Document(path)
    paragraphs = []
    for p in doc.paragraphs:
        paragraphs.append(p.text)
    return "\n".join(paragraphs)

def load_text(path):
    suffix = path.suffix.lower()
    if suffix == ".txt":
        return load_txt(path)
    elif suffix == ".pdf":
        return load_pdf(path)
    elif suffix == ".docx":
        return load_docx(path)
    else:
        raise ValueError(f"Unsupported file type: {path.name}")
if __name__ == "__main__":
    import config

    for path in config.DOCS_DIR.rglob("*"):
        if path.suffix in config.SUPPORTED_EXTENSIONS:
            text = load_text(path)
            print(path.name, "->", len(text), "characters")