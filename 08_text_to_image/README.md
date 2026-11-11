# 08 · Text to Image

Generates images from text prompts using Stable Diffusion Turbo, which makes good pictures in just 2 steps. Runs locally, from the command line or a browser interface.

## Setup
```bash
pip install -r requirements.txt
```
The model (~2 GB) downloads on first run.

**Hardware:** an NVIDIA GPU (CUDA) or Apple Silicon (MPS) is strongly recommended. CPU works but can take a minute or more per image.

## Run
Command line (images are saved to `outputs/`):
```bash
python app.py "a cozy cabin in a snowy forest, watercolor"
python app.py "neon Seoul street at night" --n 4 --seed 7
```

Browser interface:
```bash
python app.py --ui
```
Then open the local link it prints (usually http://127.0.0.1:7860).

## Options
| Flag | Meaning |
|------|---------|
| `--n` | Number of images (1–4 recommended) |
| `--seed` | Fix the seed to reproduce the same image |
| `--ui` | Launch the Gradio web app |

## Prompt tips
- Describe subject + style + lighting: "portrait of an old fisherman, oil painting, warm golden light".
- SD-Turbo outputs 512×512 images; for bigger results, try `stabilityai/sdxl-turbo` (needs more VRAM).

## Ideas to extend
- Add image-to-image editing with `AutoPipelineForImage2Image`.
- Save the prompt and seed into each PNG's metadata.
