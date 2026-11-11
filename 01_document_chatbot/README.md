# 01 · Document Chatbot

Ask questions about your own files (PDF, TXT, MD). The app finds the most relevant passages and Claude answers using only them, citing the file names.

## How it works
1. Reads every `.pdf`, `.txt` and `.md` file in a folder (including subfolders).
2. Splits the text into overlapping chunks of about 800 characters.
3. Turns each chunk into a vector with `all-MiniLM-L6-v2` (sentence-transformers).
4. For each question, picks the 4 closest chunks and sends them to Claude as context.

## Setup
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...        # Windows: set ANTHROPIC_API_KEY=sk-...
```

## Run
```bash
mkdir docs                 # put your files here
python app.py ./docs
```
```
Indexed 128 chunks from './docs'. Ask away (Ctrl+C to quit).

You: When does my lease end?
Bot: Your lease ends on 31 August 2027 [lease_contract.pdf].
```

## Options
- `CLAUDE_MODEL` environment variable changes the model.
- Change `size` / `overlap` in `chunk()` or `k` in `retrieve()` to tune answers.

## Limitations
- Scanned PDFs (images) have no text; run OCR on them first.
- The index is rebuilt each time you start the app.

## Ideas to extend
- Save the vectors to disk (e.g. with FAISS or ChromaDB) so startup is instant.
- Add a web UI with Streamlit or Gradio.
