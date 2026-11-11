"""Chat with your personal documents (PDF / TXT / MD) using retrieval + Claude.
Usage:  python app.py ./docs
"""
import os, sys, glob
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import anthropic

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")
embedder = SentenceTransformer("all-MiniLM-L6-v2")


def load_text(path):
    if path.lower().endswith(".pdf"):
        return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
    with open(path, encoding="utf-8", errors="ignore") as f:
        return f.read()


def chunk(text, size=800, overlap=150):
    pieces, i = [], 0
    while i < len(text):
        pieces.append(text[i:i + size])
        i += size - overlap
    return [p for p in pieces if p.strip()]


def build_index(folder):
    chunks, sources = [], []
    for path in glob.glob(os.path.join(folder, "**", "*"), recursive=True):
        if path.lower().endswith((".pdf", ".txt", ".md")):
            for c in chunk(load_text(path)):
                chunks.append(c)
                sources.append(os.path.basename(path))
    if not chunks:
        sys.exit(f"No .pdf/.txt/.md files found in '{folder}'")
    vectors = embedder.encode(chunks, normalize_embeddings=True, show_progress_bar=True)
    return chunks, sources, vectors


def retrieve(question, chunks, sources, vectors, k=4):
    q = embedder.encode([question], normalize_embeddings=True)[0]
    top = np.argsort(vectors @ q)[::-1][:k]
    return [(sources[i], chunks[i]) for i in top]


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "docs"
    chunks, sources, vectors = build_index(folder)
    print(f"Indexed {len(chunks)} chunks from '{folder}'. Ask away (Ctrl+C to quit).")

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    history = []
    while True:
        question = input("\nYou: ").strip()
        if not question:
            continue
        context = "\n\n".join(f"[{s}]\n{c}" for s, c in retrieve(question, chunks, sources, vectors))
        history.append({"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"})
        reply = client.messages.create(
            model=MODEL,
            max_tokens=800,
            system=("Answer using only the provided context. Cite file names in [brackets]. "
                    "If the answer is not in the context, say you couldn't find it."),
            messages=history[-5:],  # keep recent turns; always starts with a user turn
        ).content[0].text
        history.append({"role": "assistant", "content": reply})
        print(f"\nBot: {reply}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
