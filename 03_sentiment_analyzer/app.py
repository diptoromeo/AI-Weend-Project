"""Scan product reviews for sentiment.
Usage:
  python app.py reviews.csv            # CSV with a 'review' column
  python app.py "This blender is great!"
"""
import os, sys
import pandas as pd
from transformers import pipeline

# Multilingual model (works for English, Korean, etc.) -> 1 to 5 stars
classifier = pipeline("sentiment-analysis",
                      model="nlptown/bert-base-multilingual-uncased-sentiment",
                      truncation=True)


def label(stars):
    return "positive" if stars >= 4 else "negative" if stars <= 2 else "neutral"


def analyze(texts):
    results = classifier(list(texts), batch_size=16)
    stars = [int(r["label"][0]) for r in results]
    return pd.DataFrame({
        "review": texts,
        "stars": stars,
        "sentiment": [label(s) for s in stars],
        "confidence": [round(r["score"], 3) for r in results],
    })


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    arg = sys.argv[1]

    if os.path.isfile(arg):
        df_in = pd.read_csv(arg)
        col = "review" if "review" in df_in.columns else df_in.columns[0]
        df = analyze(df_in[col].astype(str).tolist())
        out = arg.rsplit(".", 1)[0] + "_sentiment.csv"
        df.to_csv(out, index=False)

        print(f"\nAnalyzed {len(df)} reviews  ->  saved {out}")
        print(f"Average rating: {df.stars.mean():.2f} / 5\n")
        print(df.sentiment.value_counts(normalize=True).mul(100).round(1).astype(str).add("%").to_string())
        print("\nMost negative reviews:")
        for r in df.sort_values("stars").head(3).review:
            print(" -", r[:120])
    else:
        r = analyze([arg]).iloc[0]
        print(f"{r.sentiment.upper()}  ({r.stars}★, confidence {r.confidence})")


if __name__ == "__main__":
    main()
