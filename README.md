# 10 AI Weekend Projects

Each folder is independent: `cd` into it, install, run.

```bash
cd 06_spam_detector
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py train
```

| # | Project | Runs offline? | Quick start |
|---|---------|---------------|-------------|
| 01 | Document chatbot | needs API key | `python app.py ./docs` |
| 02 | Resume checker | yes (AI feedback optional) | `python app.py resume.pdf job.txt` |
| 03 | Sentiment analyzer | yes | `python app.py sample_reviews.csv` |
| 04 | Image classifier | yes | `python app.py train --data data` then `python app.py predict cat.jpg` |
| 05 | YouTube summarizer | needs API key | `python app.py "https://youtu.be/..." --out Korean` |
| 06 | Spam detector | yes | `python app.py train` then `python app.py predict "Win a prize!"` |
| 07 | Voice transcriber | yes | `python app.py memo.m4a --lang ko` |
| 08 | Text to image | yes (GPU recommended) | `python app.py "a cat astronaut"` or `--ui` |
| 09 | Movie recommender | yes | `python app.py "Toy Story" "Up"` |
| 10 | Personal assistant | needs API key | `python app.py` then `/meals` |

**API key** (projects 01, 02, 05, 10): get one at https://console.anthropic.com and set it:
`export ANTHROPIC_API_KEY=sk-...` (Windows: `set ANTHROPIC_API_KEY=sk-...`).
Change the model with `CLAUDE_MODEL` if you like.

**Extra notes**
- 07 needs `ffmpeg` installed for m4a/mp3 (`brew install ffmpeg` / `apt install ffmpeg`).
- 08 downloads ~2 GB of model weights the first time. On CPU it works but is slow.
- 04: put a few hundred images per class in `data/train/<class>/` and `data/val/<class>/`.
