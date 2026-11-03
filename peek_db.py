import chromadb
import config

client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
collection = client.get_collection(config.COLLECTION_NAME)

data = collection.get()

for chunk_id, meta in zip(data["ids"], data["metadatas"]):
    print(chunk_id, "->", meta)