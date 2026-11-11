"""Summarize a YouTube video from its transcript.
Usage:  python app.py "https://www.youtube.com/watch?v=VIDEO_ID" [--lang ko]
"""
import argparse, os, re
from youtube_transcript_api import YouTubeTranscriptApi
import anthropic

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")


def video_id(url):
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([\w-]{11})", url)
    if not m:
        raise ValueError("Could not find a video ID in that URL")
    return m.group(1)


def get_transcript(vid, langs):
    fetched = YouTubeTranscriptApi().fetch(vid, languages=langs)
    lines = []
    for s in fetched:
        mins, secs = divmod(int(s.start), 60)
        lines.append(f"[{mins:02d}:{secs:02d}] {s.text}")
    return "\n".join(lines)


def summarize(transcript, out_lang):
    client = anthropic.Anthropic()
    # Long videos: summarize in parts, then combine
    parts = [transcript[i:i + 60000] for i in range(0, len(transcript), 60000)]
    notes = []
    for part in parts:
        notes.append(client.messages.create(
            model=MODEL, max_tokens=1000,
            messages=[{"role": "user", "content": f"Take concise notes (keep timestamps) on this transcript part:\n\n{part}"}],
        ).content[0].text)

    prompt = (f"Using these notes from a YouTube video, write in {out_lang}:\n"
              "1. A one-sentence TL;DR\n2. 5-8 key points with timestamps\n3. Action items or takeaways\n\n"
              + "\n\n".join(notes))
    return client.messages.create(model=MODEL, max_tokens=1200,
                                  messages=[{"role": "user", "content": prompt}]).content[0].text


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--lang", default="en", help="transcript language code, e.g. en, ko")
    ap.add_argument("--out", default="English", help="summary language, e.g. Korean")
    args = ap.parse_args()

    vid = video_id(args.url)
    transcript = get_transcript(vid, [args.lang, "en", "ko"])
    print(f"Transcript: {len(transcript):,} characters. Summarizing...\n")
    summary = summarize(transcript, args.out)
    print(summary)
    with open(f"summary_{vid}.md", "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"\nSaved summary_{vid}.md")
