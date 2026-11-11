# 05 · YouTube Summarizer

Pulls a video's transcript and writes a summary: a one-line TL;DR, key points with timestamps, and takeaways. Saves it as a Markdown file.

## How it works
1. Gets the video ID from the URL (works with normal, `youtu.be`, Shorts and embed links).
2. Downloads the transcript with `youtube-transcript-api` (no video download needed).
3. Long transcripts are split into parts, each summarized, then combined by Claude.

## Setup
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...
```

## Run
```bash
python app.py "https://www.youtube.com/watch?v=VIDEO_ID"
```
Korean video, Korean summary:
```bash
python app.py "https://youtu.be/VIDEO_ID" --lang ko --out Korean
```

## Options
| Flag | Meaning | Default |
|------|---------|---------|
| `--lang` | Preferred transcript language code | `en` |
| `--out` | Language of the summary | `English` |

Output is printed and saved as `summary_<VIDEO_ID>.md`.

## Limitations
- Only works on videos that have captions (manual or auto-generated).
- YouTube sometimes blocks transcript requests from cloud servers; run it from your own computer.

## Ideas to extend
- Add a "chat with the video" mode using the transcript as context.
- Batch-summarize every video in a playlist.
