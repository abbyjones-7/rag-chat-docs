from pypdf import PdfReader
from pathlib import Path

def load_pdf(filepath):
    reader = PdfReader(filepath)
    pages = []
    for i, page in enumerate(reader.pages, start =1):
        text = page.extract_text() or ""
        pages.append((i,text))
    return pages

def chunk_text(text, chunkSize =350, overlap=50):
    chunks = []
    start = 0
    while start<len(text):
        chunks.append(text[start:start+chunkSize])
        start += chunkSize -overlap
    return chunks

def load_and_chunk(path):
    results = []
    for page_num, text in load_pdf(path):
        for chunk in chunk_text(text):
            results.append({
                "text": chunk,
                "source": Path(path).name,
                "page": page_num
            })
    return results

if __name__ == "__main__":
    chunks = load_and_chunk("docs/SyllabusCS165_Fall2026-2.pdf")
    print(f"Made {len(chunks)} chunks")
    print(chunks[0])

