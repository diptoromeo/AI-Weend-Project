"""Text-to-image with Stable Diffusion Turbo (runs locally; GPU strongly recommended).
Usage:
  python app.py "a cozy cabin in a snowy forest, watercolor"
  python app.py "neon Seoul street at night" --n 4 --seed 7
  python app.py --ui                       # simple web UI in your browser
"""
import argparse, os, time
import torch
from diffusers import AutoPipelineForText2Image

DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

print(f"Loading model on {DEVICE}...")
pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sd-turbo", torch_dtype=DTYPE).to(DEVICE)


def generate(prompt, n=1, seed=None):
    gen = torch.Generator(DEVICE).manual_seed(seed) if seed is not None else None
    # SD-Turbo makes good images in 1-4 steps without guidance
    return pipe(prompt=[prompt] * n, num_inference_steps=2, guidance_scale=0.0, generator=gen).images


def cli(prompt, n, seed):
    os.makedirs("outputs", exist_ok=True)
    for i, img in enumerate(generate(prompt, n, seed)):
        path = f"outputs/{int(time.time())}_{i}.png"
        img.save(path)
        print("Saved", path)


def ui():
    import gradio as gr
    gr.Interface(
        fn=lambda p, n, s: generate(p, int(n), int(s) if s else None),
        inputs=[gr.Textbox(label="Prompt"), gr.Slider(1, 4, 1, step=1, label="Images"),
                gr.Number(label="Seed (optional)", value=None)],
        outputs=gr.Gallery(label="Results"),
        title="Text → Image",
    ).launch()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt", nargs="?")
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--ui", action="store_true")
    args = ap.parse_args()
    ui() if args.ui or not args.prompt else cli(args.prompt, args.n, args.seed)
