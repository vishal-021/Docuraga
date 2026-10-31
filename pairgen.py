"""
Step 1: build a training/test dataset from your PDFs.

For each chunk of each PDF, a local LLM (qwen3 via ollama) writes a few
questions that the chunk answers. Result:
    dl_data/chunks.json   every chunk, with a train/test split label
    dl_data/pairs.jsonl   (question, chunk_id, split) rows

Usage:
    python pairgen.py --pdfs workspaces/project/pdfs --max-chunks 400 --per-chunk 3
Re-running resumes where it stopped.
"""
import os
import json
import random
import argparse

import fitz
import ollama
from pydantic import BaseModel

import config


class Questions(BaseModel):
    questions: list[str]


def chunk_text(text, size, overlap):
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks


def load_chunks(pdf_folder):
    chunks = []
    for filename in sorted(os.listdir(pdf_folder)):
        if not filename.lower().endswith(".pdf"):
            continue
        doc = fitz.open(os.path.join(pdf_folder, filename))
        for page_no, page in enumerate(doc, start=1):
            for i, c in enumerate(chunk_text(page.get_text(), config.CHUNK_SIZE, config.CHUNK_OVERLAP)):
                if len(c.strip()) < config.MIN_CHUNK_CHARS:
                    continue
                chunks.append({"id": len(chunks), "pdf": filename,
                               "page": page_no, "chunk": i, "text": c})
        doc.close()
    return chunks


def assign_splits(chunks, test_frac, seed):
    """Split by PDF when there are enough PDFs (hardest, most honest test),
    otherwise by random chunk."""
    rng = random.Random(seed)
    pdfs = sorted({c["pdf"] for c in chunks})
    if len(pdfs) >= 5:
        rng.shuffle(pdfs)
        n_test = max(1, round(len(pdfs) * test_frac))
        test_pdfs = set(pdfs[:n_test])
        for c in chunks:
            c["split"] = "test" if c["pdf"] in test_pdfs else "train"
        mode = "by PDF"
    else:
        for c in chunks:
            c["split"] = "test" if rng.random() < test_frac else "train"
        mode = "by chunk"
    return mode


BAD = ("the passage", "the text", "this text", "the excerpt", "the document", "the above", "this passage")


def make_questions(chunk_text_, n):
    prompt = (
        f"Write {n} different questions that can be answered using ONLY the passage below.\n"
        "Rules: each question must make sense on its own, without seeing the passage. "
        "Never say 'the passage', 'the text' or 'the document'. Name the specific topic, "
        "term or entity. Vary the style (what, why, how, define, compare).\n\n"
        f"Passage:\n{chunk_text_}"
    )
    resp = ollama.chat(
        model=config.LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        format=Questions.model_json_schema(),
        think=False,
        options={"temperature": 0.4},
    )
    qs = Questions.model_validate_json(resp["message"]["content"]).questions
    out = []
    for q in qs:
        q = q.strip()
        if len(q) < 15 or any(b in q.lower() for b in BAD):
            continue
        out.append(q)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdfs", required=True, help="folder with PDFs")
    ap.add_argument("--max-chunks", type=int, default=400, help="how many chunks to write questions for")
    ap.add_argument("--per-chunk", type=int, default=3)
    ap.add_argument("--test-frac", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    os.makedirs(config.DATA_DIR, exist_ok=True)
    chunks_path = os.path.join(config.DATA_DIR, "chunks.json")
    pairs_path = os.path.join(config.DATA_DIR, "pairs.jsonl")

    chunks = []
    if os.path.exists(chunks_path):
        chunks = json.load(open(chunks_path, encoding="utf-8"))
        print(f"Loaded {len(chunks)} existing chunks (delete {chunks_path} to rebuild)")
    if not chunks:
        if not os.path.isdir(args.pdfs):
            raise SystemExit(f"PDF folder not found: {args.pdfs}")
        chunks = load_chunks(args.pdfs)
        if not chunks:
            raise SystemExit(f"No readable text in PDFs under {args.pdfs}. "
                             "Are there .pdf files, and are they text (not scanned images)?")
        mode = assign_splits(chunks, args.test_frac, args.seed)
        json.dump(chunks, open(chunks_path, "w", encoding="utf-8"))
        print(f"{len(chunks)} chunks, split {mode}")

    if not chunks:
        raise SystemExit("No chunks found. Check the PDF folder.")

    done = set()
    if os.path.exists(pairs_path):
        for line in open(pairs_path, encoding="utf-8"):
            done.add(json.loads(line)["chunk_id"])

    rng = random.Random(args.seed)
    order = [c for c in chunks]
    rng.shuffle(order)
    targets = order[:args.max_chunks]

    with open(pairs_path, "a", encoding="utf-8") as f:
        for n, c in enumerate(targets, start=1):
            if c["id"] in done:
                continue
            try:
                qs = make_questions(c["text"], args.per_chunk)
            except Exception as e:
                print(f"[{n}/{len(targets)}] failed: {e}")
                continue
            for q in qs:
                f.write(json.dumps({"question": q, "chunk_id": c["id"], "split": c["split"]},
                                   ensure_ascii=False) + "\n")
            f.flush()
            print(f"[{n}/{len(targets)}] chunk {c['id']} ({c['split']}): {len(qs)} questions")

    rows = [json.loads(l) for l in open(pairs_path, encoding="utf-8")]
    tr = sum(r["split"] == "train" for r in rows)
    print(f"\nDone. {tr} train pairs, {len(rows) - tr} test pairs -> {pairs_path}")


if __name__ == "__main__":
    main()
