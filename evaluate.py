"""
Step 3: compare retrieval systems on the held-out TEST questions.

Systems:
    bm25                 keyword baseline
    minilm               small general embedding model
    bge-base             pretrained bge
    bge-finetuned        your fine-tuned bge (if models/bge-finetuned exists)
    <dense> + rerank     cross-encoder rescoring of the top candidates

Metrics: Recall@1/5/10 and MRR@10 (gold = the chunk the question was written from).
Usage:   python evaluate.py            (add --no-rerank to skip the cross-encoder)
Output:  table in the terminal + dl_data/results.csv
"""
import os
import re
import csv
import json
import argparse

import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder
from rank_bm25 import BM25Okapi

import config

TOP = 20  # candidates kept per query (also what the reranker sees)


def compute_metrics(rankings, golds):
    """rankings: list of lists of chunk ids (best first). golds: list of chunk ids."""
    r1 = r5 = r10 = mrr = 0.0
    for ranked, gold in zip(rankings, golds):
        top10 = ranked[:10]
        if gold in top10:
            r10 += 1
            mrr += 1.0 / (top10.index(gold) + 1)
        r5 += gold in ranked[:5]
        r1 += gold in ranked[:1]
    n = len(golds)
    return {"Recall@1": r1 / n, "Recall@5": r5 / n, "Recall@10": r10 / n, "MRR@10": mrr / n}


def dense_rank(model_name, prefix, corpus_texts, queries):
    model = SentenceTransformer(model_name)
    c = model.encode(corpus_texts, normalize_embeddings=True, batch_size=32, show_progress_bar=True)
    q = model.encode([prefix + x for x in queries], normalize_embeddings=True, batch_size=32)
    scores = q @ c.T
    return [list(np.argsort(-row)[:TOP]) for row in scores]


def bm25_rank(corpus_texts, queries):
    tok = lambda s: re.findall(r"\w+", s.lower())
    bm = BM25Okapi([tok(t) for t in corpus_texts])
    return [list(np.argsort(-bm.get_scores(tok(q)))[:TOP]) for q in queries]


def rerank(ce, corpus_texts, queries, candidate_lists):
    out = []
    for q, cands in zip(queries, candidate_lists):
        scores = ce.predict([(q, corpus_texts[i]) for i in cands], batch_size=16)
        out.append([cands[i] for i in np.argsort(-np.asarray(scores))])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-rerank", action="store_true")
    args = ap.parse_args()

    chunks = json.load(open(os.path.join(config.DATA_DIR, "chunks.json"), encoding="utf-8"))
    pairs = [json.loads(l) for l in open(os.path.join(config.DATA_DIR, "pairs.jsonl"), encoding="utf-8")]
    test = [p for p in pairs if p["split"] == "test"]
    if not test:
        raise SystemExit("No test pairs. Run pairgen.py first.")

    # corpus = ALL chunks (train + test), so retrieval is as hard as in the real app
    ids = [c["id"] for c in chunks]
    texts = [c["text"] for c in chunks]
    pos = {cid: i for i, cid in enumerate(ids)}
    queries = [p["question"] for p in test]
    golds = [pos[p["chunk_id"]] for p in test]
    print(f"{len(test)} test questions against {len(texts)} chunks\n")

    results = {}
    dense_cache = {}

    results["bm25"] = bm25_rank(texts, queries)

    systems = [
        ("minilm", "sentence-transformers/all-MiniLM-L6-v2", ""),
        ("bge-base", "BAAI/bge-base-en-v1.5", config.QUERY_PREFIX),
    ]
    if os.path.isdir(config.FINETUNED_DIR):
        systems.append(("bge-finetuned", config.FINETUNED_DIR, config.QUERY_PREFIX))
    else:
        print("(no fine-tuned model found, skipping bge-finetuned)\n")

    for name, path, prefix in systems:
        print("Encoding with", name)
        dense_cache[name] = dense_rank(path, prefix, texts, queries)
        results[name] = dense_cache[name]

    if not args.no_rerank:
        print("Loading reranker", config.RERANK_MODEL)
        ce = CrossEncoder(config.RERANK_MODEL)
        for name in ("bge-base", "bge-finetuned"):
            if name in dense_cache:
                print("Reranking", name)
                results[name + " + rerank"] = rerank(ce, texts, queries, dense_cache[name])

    rows = []
    for name, ranking in results.items():
        m = compute_metrics(ranking, golds)
        rows.append({"system": name, **{k: round(v, 4) for k, v in m.items()}})

    header = ["system", "Recall@1", "Recall@5", "Recall@10", "MRR@10"]
    print("\n" + "".join(h.ljust(24 if i == 0 else 12) for i, h in enumerate(header)))
    for r in rows:
        print("".join(str(r[h]).ljust(24 if i == 0 else 12) for i, h in enumerate(header)))

    out = os.path.join(config.DATA_DIR, "results.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        w.writerows(rows)
    print("\nSaved", out)


if __name__ == "__main__":
    main()
