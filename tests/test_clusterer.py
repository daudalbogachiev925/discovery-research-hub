import numpy as np
from app.nlp.clusterer import cluster, top_terms

def test_cluster_labels():
    vecs = np.random.rand(20, 16)
    labels = cluster(vecs, n_clusters=3)
    assert len(labels) == 20
    assert len(set(labels)) <= 3

def test_top_terms():
    texts = ["ai fast", "ai simple", "retail slow", "retail boring"]
    labels = [0, 0, 1, 1]
    terms = top_terms(texts, labels, k=3)
    assert 0 in terms and 1 in terms
