import os
import pickle
import fitz
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer, CrossEncoder

import config

# Embedding model comes from config.py. After fine-tuning, set
# EMBED_MODEL = "models/bge-finetuned" there and rebuild each workspace's index.
model = SentenceTransformer(config.EMBED_MODEL)

dimension = model.get_embedding_dimension()

_reranker = None


def get_reranker():
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder(config.RERANK_MODEL)
    return _reranker


def extract_pdf(pdf_path):

    doc = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(doc):

        text = page.get_text()

        pages.append({
            "page": page_number + 1,
            "text": text
        })

    doc.close()

    return pages


def chunk_text(text, size, overlap):

    chunks = []

    start = 0

    while start < len(text):

        end = start + size

        chunks.append(text[start:end])

        start += size - overlap

    return chunks

#Call this once for everytime u obtain new pdfs
def BuildIndex(faissPath,pdfFolder,metadataPath = "metadata.pkl"):

    index = faiss.IndexFlatIP(dimension)

    metadata = []

    for filename in os.listdir(pdfFolder):

        if not filename.lower().endswith(".pdf"):
            continue

        path = os.path.join(pdfFolder, filename)

        print("Reading:", filename)

        pages = extract_pdf(path)

        for page in pages:

            chunks = chunk_text(page["text"], size=config.CHUNK_SIZE, overlap=config.CHUNK_OVERLAP)

            keep = [(n, c) for n, c in enumerate(chunks) if len(c.strip()) >= 50]
            if not keep:
                continue

            # encode all chunks of the page in one batch (much faster than one by one)
            embeddings = model.encode(
                [c for _, c in keep],
                normalize_embeddings=True
            ).astype(np.float32)

            index.add(embeddings)

            for chunk_number, chunk in keep:
                metadata.append({
                    "pdf": filename,
                    "page": page["page"],
                    "chunk": chunk_number,
                    "text": chunk
                })

    faiss.write_index(index, faissPath)

    with open(metadataPath, "wb") as f:
        pickle.dump(metadata, f)

    print()

    print("Finished")
    print("Vectors:", index.ntotal)


def load_index(faissPath,metadataPath):

    if not os.path.exists(faissPath):
        raise FileNotFoundError(
            "No index yet. Add PDFs and click 'Index Folder' (or use Gather) first."
        )

    index = faiss.read_index(faissPath)

    with open(metadataPath, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata


def Search(faissPath, metaPath,question, k=5):

    index, metadata = load_index(faissPath,metaPath)

    if index.ntotal == 0:
        return []

    query = model.encode(
        config.QUERY_PREFIX + question,
        normalize_embeddings=True
    ).astype(np.float32)

    # fetch more candidates when reranking, then keep the best k
    n_fetch = max(k, config.RERANK_CANDIDATES) if config.USE_RERANKER else k

    scores, ids = index.search(
        query.reshape(1, -1),
        min(n_fetch, index.ntotal)
    )

    candidates = []

    for score, idx in zip(scores[0], ids[0]):

        if idx == -1:
            continue

        candidates.append({
            "score": float(score),
            "pdf": metadata[idx]["pdf"],
            "page": metadata[idx]["page"],
            "text": metadata[idx]["text"]
        })

    if config.USE_RERANKER and candidates:
        ce_scores = get_reranker().predict([(question, c["text"]) for c in candidates])
        for c, s in zip(candidates, ce_scores):
            c["score"] = float(s)
        candidates.sort(key=lambda c: c["score"], reverse=True)

    return candidates[:k]

#returns prompt and result of RAG
def BuildPrompt(faissPath,metaPath,question,res = 5):

    results = Search(faissPath,metaPath,question,res)

    context = ""

    for r in results:

        context += (
            f"Source: {r['pdf']} "
            f"(Page {r['page']})\n"
        )

        context += r["text"]

        context += "\n\n"

    prompt = f"""
    You are answering questions using ONLY the supplied context.

    If the answer cannot be found,
    say you do not know.

    Context:

    {context}

    Question:

    {question}

    Answer:
    """

    return prompt,results