# 09 · Movie Recommender

Suggests movies you might like based on one or more favorites. Uses the MovieLens "small" dataset (about 9,700 movies and 100,000 ratings). Fully offline after download.

## How it works
It's a hybrid recommender that mixes two signals:
- **Collaborative (60%):** movies that the same users rated similarly (user-centered ratings + cosine similarity).
- **Content (40%):** similar genres and user tags (TF-IDF + cosine similarity).

Scores are boosted for movies with more ratings, so obscure titles with one review don't dominate.

## Setup
```bash
pip install -r requirements.txt
```

## Run
```bash
python app.py "Toy Story"
python app.py "Inception" "The Matrix" --n 15
```
```
Based on: Inception (2010), Matrix, The (1999)

 1. Dark Knight, The (2008)        ⭐ 4.2  (Action, Crime, Drama, IMAX)
 2. Interstellar (2014)            ⭐ 4.0  (Sci-Fi, IMAX)
 ...
```
Title search is partial and case-insensitive; if several match, the most-rated one is used.

## Limitations
- The dataset only covers movies up to around 2018.
- For books, swap in a dataset like Goodreads or Book-Crossing with the same structure.

## Ideas to extend
- Let users rate a few movies and recommend from their personal ratings.
- Add movie posters with the TMDB API and build a Streamlit page.
