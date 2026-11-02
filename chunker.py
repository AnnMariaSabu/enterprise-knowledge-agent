def split_text(text, size, overlap):
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    words = text.split()
    step = size - overlap
    chunks = []
    start = 0

    while start < len(words):
        chunk_words = words[start:start + size]
        chunks.append(" ".join(chunk_words))
        if start + size >= len(words):
            break
        start = start + step

    return chunks

if __name__ == "__main__":
    import config
    from loaders import load_text

    path = config.DOCS_DIR / "hr" / "hr_policy.txt"
    text = load_text(path)
    chunks = split_text(text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)

    print("Number of chunks:", len(chunks))
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i} ({len(chunk)} characters) ---")
        print(chunk)