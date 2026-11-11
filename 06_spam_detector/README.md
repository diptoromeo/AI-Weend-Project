# 06 · Spam Detector

A classic machine-learning spam filter trained on the public SMS Spam Collection dataset (about 5,500 labeled messages). Fully offline after the dataset download.

## How it works
- **Features:** TF-IDF of single words and word pairs.
- **Model:** Multinomial Naive Bayes.
- **Evaluation:** 80/20 train/test split with a precision/recall report.

## Setup
```bash
pip install -r requirements.txt
```

## Train
```bash
python app.py train
```
Downloads the dataset the first time, prints the test results, and saves `spam_model.joblib`. Expect roughly 98% accuracy.

## Predict
Single message:
```bash
python app.py predict "Congratulations! You won a free iPhone, click here"
```
```
🚫 SPAM (99%)  Congratulations! You won a free iPhone, click here
```
A file with one message per line:
```bash
python app.py predict emails.txt
```

## Limitations
- Trained on English SMS messages, so it's weaker on long emails or other languages.
- To specialize it, retrain on your own labeled emails (same `label` / `text` format).

## Ideas to extend
- Compare with Logistic Regression or a small transformer model.
- Connect it to your inbox with the Gmail API to auto-label messages.
