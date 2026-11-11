"""Cats vs dogs (or any classes) image classifier with transfer learning.

Folder layout for training:
  data/train/cats/*.jpg   data/train/dogs/*.jpg
  data/val/cats/*.jpg     data/val/dogs/*.jpg
(Download: https://www.kaggle.com/c/dogs-vs-cats  — a few hundred images per class is enough.)

Usage:
  python app.py train --data data --epochs 5
  python app.py predict photo.jpg
"""
import argparse, json
import torch
from torch import nn
from torchvision import datasets, models, transforms
from PIL import Image

DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
NORM = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
TRAIN_TF = transforms.Compose([transforms.RandomResizedCrop(224), transforms.RandomHorizontalFlip(),
                               transforms.ToTensor(), NORM])
EVAL_TF = transforms.Compose([transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor(), NORM])


def build_model(num_classes):
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    for p in model.parameters():
        p.requires_grad = False                     # freeze pretrained backbone
    model.fc = nn.Linear(model.fc.in_features, num_classes)  # train only the head
    return model.to(DEVICE)


def train(data_dir, epochs):
    train_ds = datasets.ImageFolder(f"{data_dir}/train", TRAIN_TF)
    val_ds = datasets.ImageFolder(f"{data_dir}/val", EVAL_TF)
    train_dl = torch.utils.data.DataLoader(train_ds, batch_size=32, shuffle=True, num_workers=2)
    val_dl = torch.utils.data.DataLoader(val_ds, batch_size=32, num_workers=2)

    model = build_model(len(train_ds.classes))
    opt = torch.optim.Adam(model.fc.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()

    for epoch in range(epochs):
        model.train()
        for x, y in train_dl:
            x, y = x.to(DEVICE), y.to(DEVICE)
            opt.zero_grad()
            loss = loss_fn(model(x), y)
            loss.backward()
            opt.step()

        model.eval()
        correct = total = 0
        with torch.no_grad():
            for x, y in val_dl:
                pred = model(x.to(DEVICE)).argmax(1).cpu()
                correct += (pred == y).sum().item()
                total += len(y)
        print(f"Epoch {epoch + 1}/{epochs}  loss {loss.item():.3f}  val acc {correct / total:.1%}")

    torch.save(model.state_dict(), "model.pt")
    json.dump(train_ds.classes, open("classes.json", "w"))
    print("Saved model.pt and classes.json")


def predict(image_path):
    classes = json.load(open("classes.json"))
    model = build_model(len(classes))
    model.load_state_dict(torch.load("model.pt", map_location=DEVICE))
    model.eval()
    x = EVAL_TF(Image.open(image_path).convert("RGB")).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        probs = torch.softmax(model(x), 1)[0]
    for cls, p in sorted(zip(classes, probs.tolist()), key=lambda t: -t[1]):
        print(f"{cls:>10}: {p:.1%}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("train"); t.add_argument("--data", default="data"); t.add_argument("--epochs", type=int, default=5)
    p = sub.add_parser("predict"); p.add_argument("image")
    args = ap.parse_args()
    train(args.data, args.epochs) if args.cmd == "train" else predict(args.image)
