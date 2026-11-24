from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path = "chroma_db")
collection = client.get_collection("docs")

def search(question, k=3):
    query_embedding = model.encode([question]).tolist()
    results = collection.query(query_embeddings = query_embedding, n_results=k)
    texts = results["documents"][0]
    metas = results["metadatas"][0]
    return list(zip(texts, metas))

if __name__ == "__main__":
    question = "when does class meet?"
    for text, meta in search(question):
        print(f"[{meta["source"]}, page{meta["page"]}]")
        print(text)
        print("---")