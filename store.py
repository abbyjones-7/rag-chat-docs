from ingest import load_and_chunk
from sentence_transformers import SentenceTransformer
import chromadb

def build_index(pdf_path):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_or_create_collection("docs")
    chunks = load_and_chunk(pdf_path)
    print(f"Loaded {len(chunks)} chunks")

    texts = []
    metadatas =[]
    ids = []
    for i, chunk in enumerate(chunks):
        if not chunk["text"].strip():
            continue
        texts.append(chunk["text"])
        metadatas.append({"source": chunk["source"], "page": chunk["page"]})
        ids.append(f"{chunk["source"]}--{chunk["page"]}--{i}")
    print(f"Embedding {len(texts)} non-empty chunks")
    embeddings = model.encode(texts).tolist()
    collection.upsert(
        ids = ids,
        documents = texts,
        embeddings = embeddings,
        metadatas = metadatas,
    )
    print(f"Stored {len(texts)} chunks")

if __name__ == "__main__":
    build_index("docs/SyllabusCS165_Fall2026-2.pdf")
