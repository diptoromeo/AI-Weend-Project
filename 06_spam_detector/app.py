"""Spam detector trained on the public SMS Spam Collection dataset.
Usage:
  python app.py train
  python app.py predict "Congratulations! You won a free iPhone, click here"
  python app.py predict emails.txt      # one message per line
"""
import io, os, sys, urllib.request, zipfile
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report

DATA_URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"
MODEL_PATH = "spam_model.joblib"


def load_data():
    if not os.path.exists("SMSSpamCollection"):
        print("Downloading dataset...")
        raw = urllib.request.urlopen(DATA_URL).read()
        zipfile.ZipFile(io.BytesIO(raw)).extract("SMSSpamCollection")
    return pd.read_csv("SMSSpamCollection", sep="\t", names=["label", "text"], quoting=3)


def train():
    df = load_data()
    X_tr, X_te, y_tr, y_te = train_test_split(df.text, df.label, test_size=0.2,
                                              stratify=df.label, random_state=42)
    model = make_pipeline(
        TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=2, sublinear_tf=True),
        MultinomialNB(alpha=0.1),
    )
    model.fit(X_tr, y_tr)
    print(classification_report(y_te, model.predict(X_te), digits=3))
    joblib.dump(model, MODEL_PATH)
    print(f"Saved {MODEL_PATH}")


def predict(arg):
    model = joblib.load(MODEL_PATH)
    messages = open(arg, encoding="utf-8").read().splitlines() if os.path.isfile(arg) else [arg]
    for msg, probs in zip(messages, model.predict_proba(messages)):
        spam_p = probs[list(model.classes_).index("spam")]
        tag = "🚫 SPAM" if spam_p > 0.5 else "✅ HAM "
        print(f"{tag} ({spam_p:.0%})  {msg[:90]}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("train", "predict"):
        sys.exit(__doc__)
    train() if sys.argv[1] == "train" else predict(" ".join(sys.argv[2:]))
