"""Transcribe voice notes locally with Whisper (no API key needed).
Usage:
  python app.py memo.m4a                 # auto-detect language
  python app.py memo.mp3 --lang ko --model small
  python app.py recordings/              # transcribe a whole folder
Outputs a .txt (plain) and .srt (subtitles with timestamps) next to each file.
"""
import argparse, os
from faster_whisper import WhisperModel

AUDIO_EXT = (".mp3", ".m4a", ".wav", ".ogg", ".flac", ".webm", ".mp4")


def ts(seconds):
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"


def transcribe(model, path, lang):
    segments, info = model.transcribe(path, language=lang, vad_filter=True, beam_size=5)
    print(f"\n▶ {os.path.basename(path)}  (language: {info.language}, {info.duration:.0f}s)")
    base = os.path.splitext(path)[0]
    text_lines, srt = [], []
    for i, seg in enumerate(segments, 1):
        print(f"  [{seg.start:6.1f}s] {seg.text.strip()}")
        text_lines.append(seg.text.strip())
        srt.append(f"{i}\n{ts(seg.start)} --> {ts(seg.end)}\n{seg.text.strip()}\n")
    with open(base + ".txt", "w", encoding="utf-8") as f:
        f.write(" ".join(text_lines))
    with open(base + ".srt", "w", encoding="utf-8") as f:
        f.write("\n".join(srt))
    print(f"  Saved {base}.txt and {base}.srt")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--lang", default=None, help="e.g. en, ko (default: auto)")
    ap.add_argument("--model", default="base", help="tiny | base | small | medium | large-v3")
    args = ap.parse_args()

    model = WhisperModel(args.model, device="auto", compute_type="int8")
    files = ([os.path.join(args.path, f) for f in sorted(os.listdir(args.path)) if f.lower().endswith(AUDIO_EXT)]
             if os.path.isdir(args.path) else [args.path])
    for f in files:
        transcribe(model, f, args.lang)
