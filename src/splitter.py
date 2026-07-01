def chunk_text(text, chunk_size=800, overlap=150):
    """
    Break text into overlapping chunks for better retrieval.
    """

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks