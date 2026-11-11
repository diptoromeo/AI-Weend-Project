"""Movie recommender using the MovieLens dataset (hybrid: what people rate + genres).
Usage:
  python app.py "Toy Story"
  python app.py "Inception" "The Matrix" --n 15     # combine several favorites
"""
import argparse, io, os, urllib.request, zipfile
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

URL = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
DIR = "ml-latest-small"


def load():
    if not os.path.isdir(DIR):
        print("Downloading MovieLens...")
        zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(URL).read())).extractall(".")
    movies = pd.read_csv(f"{DIR}/movies.csv")
    ratings = pd.read_csv(f"{DIR}/ratings.csv")
    tags = pd.read_csv(f"{DIR}/tags.csv").groupby("movieId")["tag"].apply(lambda t: " ".join(t.astype(str)))
    movies["text"] = movies.genres.str.replace("|", " ") + " " + movies.movieId.map(tags).fillna("")
    stats = ratings.groupby("movieId").rating.agg(["mean", "count"])
    movies = movies.join(stats, on="movieId").fillna({"mean": 0, "count": 0})
    return movies.reset_index(drop=True), ratings


def build(movies, ratings):
    # Content similarity (genres + user tags)
    content = cosine_similarity(TfidfVectorizer().fit_transform(movies.text))
    # Collaborative similarity (movies rated alike by the same users)
    idx = {m: i for i, m in enumerate(movies.movieId)}
    users = {u: i for i, u in enumerate(ratings.userId.unique())}
    centered = ratings.rating - ratings.groupby("userId").rating.transform("mean")
    mat = csr_matrix((centered, (ratings.movieId.map(idx), ratings.userId.map(users))),
                     shape=(len(movies), len(users)))
    collab = cosine_similarity(mat)
    return 0.6 * collab + 0.4 * content


def find(movies, title):
    hits = movies[movies.title.str.contains(title, case=False, regex=False)]
    if hits.empty:
        raise SystemExit(f"No movie matching '{title}'")
    return hits.sort_values("count", ascending=False).index[0]


def recommend(titles, n):
    movies, ratings = load()
    sim = build(movies, ratings)
    picks = [find(movies, t) for t in titles]
    print("Based on:", ", ".join(movies.title[i] for i in picks))

    score = sim[picks].mean(axis=0)
    score = score * np.log1p(movies["count"].values)       # favor movies with enough ratings
    score[picks] = -np.inf
    top = np.argsort(score)[::-1][:n]
    print()
    for rank, i in enumerate(top, 1):
        m = movies.loc[i]
        print(f"{rank:2}. {m.title:<55} ⭐ {m['mean']:.1f}  ({m.genres.replace('|', ', ')})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("titles", nargs="+")
    ap.add_argument("--n", type=int, default=10)
    args = ap.parse_args()
    recommend(args.titles, args.n)
