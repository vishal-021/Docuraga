"""
Step 2: fine-tune the bge embedding model on (question -> chunk) pairs.

Loss: MultipleNegativesRankingLoss (in-batch negatives): every other chunk in
the batch acts as a negative for a question, so no negative mining is needed.

Install first:   pip install "sentence-transformers[train]"
Usage:           python finetune.py --epochs 3 --batch-size 16
Output:          models/bge-finetuned  (+ dl_data/training_log.json and loss_curve.png)
"""
import os
import json
import random
import argparse

import torch
from datasets import Dataset
from sentence_transformers import (
    SentenceTransformer,
    SentenceTransformerTrainer,
    SentenceTransformerTrainingArguments,
    losses,
)
from sentence_transformers.training_args import BatchSamplers

import config


def build_datasets(val_frac, seed):
    chunks = {c["id"]: c["text"] for c in json.load(open(os.path.join(config.DATA_DIR, "chunks.json"), encoding="utf-8"))}
    rows = [json.loads(l) for l in open(os.path.join(config.DATA_DIR, "pairs.jsonl"), encoding="utf-8")]
    rows = [r for r in rows if r["split"] == "train"]
    if len(rows) < 50:
        print(f"WARNING: only {len(rows)} training pairs; results will be weak. "
              "Run pairgen.py with more chunks.")

    # hold out whole chunks for validation so val loss is not trivially low
    ids = sorted({r["chunk_id"] for r in rows})
    rng = random.Random(seed)
    rng.shuffle(ids)
    val_ids = set(ids[:max(1, int(len(ids) * val_frac))])

    def to_ds(sel):
        return Dataset.from_dict({
            "anchor": [config.QUERY_PREFIX + r["question"] for r in sel],
            "positive": [chunks[r["chunk_id"]] for r in sel],
        })

    train = [r for r in rows if r["chunk_id"] not in val_ids]
    val = [r for r in rows if r["chunk_id"] in val_ids]
    return to_ds(train), to_ds(val), len(train), len(val)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="BAAI/bge-base-en-v1.5")
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--val-frac", type=float, default=0.1)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    train_ds, val_ds, n_tr, n_val = build_datasets(args.val_frac, args.seed)
    print(f"train pairs: {n_tr}   validation pairs: {n_val}   device: "
          f"{'cuda' if torch.cuda.is_available() else 'cpu'}")

    model = SentenceTransformer(args.base)
    loss = losses.MultipleNegativesRankingLoss(model)

    targs = SentenceTransformerTrainingArguments(
        output_dir="models/checkpoints",
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        learning_rate=args.lr,
        warmup_ratio=0.1,
        fp16=torch.cuda.is_available(),
        batch_sampler=BatchSamplers.NO_DUPLICATES,  # no repeated chunk inside a batch
        eval_strategy="epoch",
        save_strategy="no",
        logging_steps=5,
        report_to="none",
        seed=args.seed,
    )

    trainer = SentenceTransformerTrainer(
        model=model, args=targs, train_dataset=train_ds,
        eval_dataset=val_ds, loss=loss,
    )
    trainer.train()

    os.makedirs(config.FINETUNED_DIR, exist_ok=True)
    model.save_pretrained(config.FINETUNED_DIR)
    print("Saved fine-tuned model to", config.FINETUNED_DIR)

    log = trainer.state.log_history
    json.dump(log, open(os.path.join(config.DATA_DIR, "training_log.json"), "w"), indent=2)

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        tr = [(l["step"], l["loss"]) for l in log if "loss" in l]
        ev = [(l["step"], l["eval_loss"]) for l in log if "eval_loss" in l]
        plt.figure(figsize=(6, 4))
        if tr:
            plt.plot(*zip(*tr), label="train loss")
        if ev:
            plt.plot(*zip(*ev), "o-", label="validation loss")
        plt.xlabel("step"); plt.ylabel("loss"); plt.legend(); plt.tight_layout()
        out = os.path.join(config.DATA_DIR, "loss_curve.png")
        plt.savefig(out, dpi=150)
        print("Saved", out)
    except ImportError:
        print("matplotlib not installed; skipped loss plot (pip install matplotlib)")

    print("\nNext: set EMBED_MODEL = 'models/bge-finetuned' in config.py, rebuild the index, "
          "and run evaluate.py")


if __name__ == "__main__":
    main()
