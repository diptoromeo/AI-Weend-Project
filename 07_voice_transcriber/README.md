# 07 · Voice Note Transcriber

Turns voice memos into text using Whisper, running locally (no API key, your audio stays on your computer). Creates a plain-text transcript and an `.srt` subtitle file.

## Setup
```bash
pip install -r requirements.txt
```
Install **ffmpeg** for formats like m4a and mp3:
- macOS: `brew install ffmpeg`
- Ubuntu: `sudo apt install ffmpeg`
- Windows: `winget install ffmpeg`

## Run
```bash
python app.py memo.m4a                      # auto-detect language
python app.py memo.mp3 --lang ko            # force Korean
python app.py recordings/ --model small     # whole folder, better model
```
```
▶ memo.m4a  (language: ko, 42s)
  [   0.0s] 내일 회의는 오후 세 시로 옮겼어요.
  ...
  Saved memo.txt and memo.srt
```
Supported: mp3, m4a, wav, ogg, flac, webm, mp4.

## Choosing a model
| Model | Speed | Accuracy |
|-------|-------|----------|
| `tiny` | fastest | lowest |
| `base` (default) | fast | good for clear speech |
| `small` | medium | noticeably better, good for Korean |
| `medium` / `large-v3` | slow on CPU | best |

## Ideas to extend
- Pipe the transcript into Claude for a summary or to-do list.
- Watch a folder and transcribe new recordings automatically.
