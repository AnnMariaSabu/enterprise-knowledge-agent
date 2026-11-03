import hashlib  # NEW

import chromadb
import ollama

import config
from loaders import load_text
from chunker import split_text


def file_hash(path):  # NEW
    return hashlib.sha256(path.read_bytes()).hexdigest()


def get_metadata(path):
    relative = path.relative_to(config.DOCS_DIR)
    parts = relative.parts
    department = parts[0]

    if "restricted" in parts:
        access = "restricted"
    else:
        access = "public"

    return {
        "source": relative.as_posix(),
        "department": department,
        "access": access,
        "file_hash": file_hash(path),  # NEW
    }


def embed_chunks(chunks):
    labelled = []
    for chunk in chunks:
        labelled.append("search_document: " + chunk)
    response = ollama.embed(model=config.EMBED_MODEL, input=labelled)
    return response["embeddings"]

def get_stored_hashes(collection):
    stored = {}
    data = collection.get()
    for meta in data["metadatas"]:
        stored[meta["source"]] = meta["file_hash"]
    return stored
def run_ingest():
    client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    collection = client.get_or_create_collection(
        name=config.COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    stored_hashes = get_stored_hashes(collection)
    print("Files already in the database:", len(stored_hashes))

    seen_sources = set()

    for path in config.DOCS_DIR.rglob("*"):
        if path.suffix.lower() in config.SUPPORTED_EXTENSIONS:
            metadata = get_metadata(path)
            source = metadata["source"]
            seen_sources.add(source)

            if stored_hashes.get(source) == metadata["file_hash"]:
                print(source, "-> unchanged, skipped")
                continue

            collection.delete(where={"source": source})

            text = load_text(path)
            chunks = split_text(text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
            embeddings = embed_chunks(chunks)

            ids = []
            metadatas = []
            for i, chunk in enumerate(chunks):
                ids.append(f"{source}::{i}")
                chunk_metadata = dict(metadata)
                chunk_metadata["chunk_index"] = i
                metadatas.append(chunk_metadata)

            collection.upsert(
                ids=ids,
                documents=chunks,
                embeddings=embeddings,
                metadatas=metadatas,
            )
            print(source, "->", len(chunks), "chunks saved")

    for source in stored_hashes:
        if source not in seen_sources:
            collection.delete(where={"source": source})
            print(source, "-> removed (file no longer exists)")

    print("Total chunks in database:", collection.count())


if __name__ == "__main__":
    run_ingest()