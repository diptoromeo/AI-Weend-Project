# 03 · Sentiment Analyzer

Reads product reviews and labels each one positive, neutral or negative with a 1–5 star rating. Works for English, Korean and several other languages. Runs fully offline after the first model download.

## How it works
Uses the Hugging Face model `nlptown/bert-base-multilingual-uncased-sentiment`, which predicts 1–5 stars. Stars 4–5 = positive, 3 = neutral, 1–2 = negative.

## Setup
```bash
pip install -r requirements.txt
```
The model (~670 MB) downloads automatically on first run.

## Run
Analyze a CSV file (uses the `review` column, or the first column if there isn't one):
```bash
python app.py sample_reviews.csv
```
```
Analyzed 5 reviews  ->  saved sample_reviews_sentiment.csv
Average rating: 3.00 / 5

positive    40.0%
negative    40.0%
neutral     20.0%
```

Analyze a single sentence:
```bash
python app.py "배송이 빠르고 품질도 좋아요"
```

## Output
`<file>_sentiment.csv` with columns: `review`, `stars`, `sentiment`, `confidence`.

## Ideas to extend
- Plot the sentiment split with matplotlib.
- Group results by product or by month to spot trends.
