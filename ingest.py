import chromadb
import ollama

import config
from loaders import load_text
from chunker import split_text


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
    }


def embed_chunks(chunks):
    labelled = []
    for chunk in chunks:
        labelled.append("search_document: " + chunk)
    response = ollama.embed(model=config.EMBED_MODEL, input=labelled)
    return response["embeddings"]


if __name__ == "__main__":
    client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    collection = client.get_or_create_collection(
        name=config.COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    for path in config.DOCS_DIR.rglob("*"):
        if path.suffix.lower() in config.SUPPORTED_EXTENSIONS:
            metadata = get_metadata(path)
            text = load_text(path)
            chunks = split_text(text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
            embeddings = embed_chunks(chunks)

            ids = []
            metadatas = []
            for i, chunk in enumerate(chunks):
                ids.append(f"{metadata['source']}::{i}")
                chunk_metadata = dict(metadata)
                chunk_metadata["chunk_index"] = i
                metadatas.append(chunk_metadata)

            collection.upsert(
                ids=ids,
                documents=chunks,
                embeddings=embeddings,
                metadatas=metadatas,
            )
            print(metadata["source"], "->", len(chunks), "chunks saved")

    print("Total chunks in database:", collection.count())