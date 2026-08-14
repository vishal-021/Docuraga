import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-base-en-v1.5")

index = faiss.IndexFlatIP(768)

def Filter(query, pages,
                      relevance_threshold=0.45,
                      duplicate_threshold=0.90):

    embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    accepted_pages = []
    accepted_embeddings = []

    for page in pages:

        text = f"""
        Title:
        {page.get('title', '')}

        Description:
        {page.get('description', '')}
        Markdown:
        {page.get('markdown','')}
        """

        page_embedding = model.encode(
            text,
            normalize_embeddings=True
        )

        relevance = np.dot(embedding, page_embedding)

        if relevance < relevance_threshold:
            continue

        duplicate = False

        if index.ntotal == 0:
            duplicate = False

        scores, _ = index.search(
            page_embedding.reshape(1, -1),
            k=1
        )

        duplicate = scores[0][0] > duplicate_threshold

        if duplicate:
            continue
        index.add(page_embedding.reshape(1, -1))
        accepted_pages.append(page)
        accepted_embeddings.append(page_embedding)

    return accepted_pages