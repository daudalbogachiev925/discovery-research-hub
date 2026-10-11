import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from app.config import settings

def cluster(vectors: np.ndarray, n_clusters: int = None) -> np.ndarray:
    n = n_clusters or min(settings.N_CLUSTERS, len(vectors))
    km = KMeans(n_clusters=n, random_state=42, n_init=10)
    return km.fit_predict(vectors)

def top_terms(texts, labels, k=6):
    vec = TfidfVectorizer(max_features=2000, ngram_range=(1, 2), min_df=1)
    X = vec.fit_transform(texts)
    terms = vec.get_feature_names_out()
    result = {}
    for label in set(labels):
        mask = np.array(labels) == label
        mean = np.asarray(X[mask].mean(axis=0)).ravel()
        idx = mean.argsort()[::-1][:k]
        result[int(label)] = [terms[i] for i in idx]
    return result
