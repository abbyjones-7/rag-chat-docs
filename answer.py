import anthropic
from search import search

client = anthropic.Anthropic()

def ask(question, k=5):
    results = search(question, k=k)
    context = ""
    for text, meta in results:
        context += f"[{meta["source"]}, page{meta["page"]}]\n{text}\n\n"
    prompt = (
        "Answer the question using only the context below. "
        "If the answer isn't in the context, say you don't know. "
        "Cite the page numbers you used.\n\n"
        f"Context: \n{context}\n"
        f"Questoin: {question}"
    )
    response = client.messages.create(
        model = "claude-haiku-5-5",
        max_tokens = 500,
        messages = [{"role": "user", "content": prompt}],
    )
    answer = ""
    for block in response.content:
        if block.type == "text":
            answer += block.text
    return answer, results

if __name__ == "__main__":
    answer, sources = ask("what is the grading breakdown?")
    print(answer)
    print("\nSources:")
    for text, meta in sources:
        print(f"- {meta['source']}, page {meta['page']}")
    