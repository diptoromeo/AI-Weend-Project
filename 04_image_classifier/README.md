# 04 · Image Classifier (Cats vs Dogs)

Trains an image classifier using transfer learning: a ResNet-18 pretrained on ImageNet, with only the final layer retrained on your images. It works for cats vs dogs or any categories you choose.

## Setup
```bash
pip install -r requirements.txt
```

## Prepare data
Get images from the Kaggle Dogs vs Cats dataset (https://www.kaggle.com/c/dogs-vs-cats) or use your own. A few hundred per class is enough. Arrange them like this:
```
data/
  train/
    cats/  001.jpg 002.jpg ...
    dogs/  001.jpg 002.jpg ...
  val/
    cats/  ...
    dogs/  ...
```
Folder names become the class names, so you can add more classes (e.g. `rabbits/`).

## Train
```bash
python app.py train --data data --epochs 5
```
```
Epoch 1/5  loss 0.214  val acc 95.8%
...
Saved model.pt and classes.json
```

## Predict
```bash
python app.py predict my_pet.jpg
```
```
      cats: 97.3%
      dogs: 2.7%
```

## Notes
- Uses a GPU (CUDA or Apple MPS) automatically when available; CPU works but is slower.
- On Windows, if training hangs, set `num_workers=0` in the DataLoaders.

## Ideas to extend
- Unfreeze the last ResNet block for higher accuracy.
- Wrap `predict` in a Gradio app so you can drag and drop photos.
