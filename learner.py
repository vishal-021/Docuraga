import os
import pickle
import fitz
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-base-en-v1.5")

dimension = model.get_embedding_dimension()


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


def chunk_text(text, size,overlap):

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

            chunks = chunk_text(page["text"],size=800, overlap=100)

            for chunk_number, chunk in enumerate(chunks):

                if len(chunk.strip()) < 50:
                    continue

                embedding = model.encode(
                    chunk,
                    normalize_embeddings=True
                ).astype(np.float32)

                index.add(
                    embedding.reshape(1, -1)
                )

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

    index = faiss.read_index(faissPath)

    with open(metadataPath, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata


def Search(faissPath, metaPath,question, k=5):

    index, metadata = load_index(faissPath,metaPath)

    query = model.encode(
        question,
        normalize_embeddings=True
    ).astype(np.float32)

    scores, ids = index.search(
        query.reshape(1, -1),
        k
    )

    results = []

    for score, idx in zip(scores[0], ids[0]):

        if idx == -1:
            continue

        results.append({
            "score": float(score),
            "pdf": metadata[idx]["pdf"],
            "page": metadata[idx]["page"],
            "text": metadata[idx]["text"]
        })

    return results

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
