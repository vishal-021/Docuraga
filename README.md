# Docuraga: PDF Question Answering with a Fine-Tuned Retrieval Model

Docuraga is a desktop application that answers questions from a user’s own PDF documents. The user uploads PDFs into a workspace, asks questions in plain English, and gets answers grounded in those documents, along with the source file and page reference. Everything runs locally: the language model runs through Ollama, and no document leaves the computer.

## How It Works

The application utilizes Retrieval-Augmented Generation (RAG) split into three distinct stages:
* **Indexing:** PDF text is extracted using `PyMuPDF` and split into overlapping 800-character chunks. A transformer embedding model (`BAAI/bge-base-en-v1.5`) converts each chunk into a 768-dimensional vector, and the vectors are stored in a FAISS index.
* **Retrieval:** A user question is embedded using the same model, and the most similar chunks are surfaced via vector search. An optional cross-encoder reranker rescores the top candidates for maximum precision.
* **Answer Generation:** The highest-ranking chunks are passed to a local LLM (`Qwen3` via Ollama), which is strictly instructed to answer only from that context or state when the answer cannot be found.

## Deep Learning Component

Instead of relying solely on the pretrained embedding model unchanged, Docuraga fine-tunes it directly on the user’s unique documents:
* **Synthetic Data Generation:** The local LLM generates questions for each extracted chunk, producing distinct question-and-passage pairs which are partitioned into train and test splits.
* **Fine-Tuning:** The embedding model is trained via contrastive learning (`MultipleNegativesRankingLoss` using in-batch negatives), pulling each question's vector closer to its corresponding source passage.
* **Evaluation:** On held-out validation questions, the system evaluates and benchmarks `BM25`, `MiniLM`, `base bge`, and `fine-tuned bge` (each with and without a reranker) using Metrics like Recall@1/5/10 and MRR@10.
* **Automatic Selection:** The system intelligently switches to the fine-tuned model *only* if it outperforms the base model. Otherwise, the application safely preserves the standard configuration.

## Ease of Use

The entire pipeline—encompassing question generation, training, testing, model selection, and re-indexing—is abstracted behind a single button in the interface: **Train on my PDFs**. It requires no terminal intervention, and each workspace manages and retains its own custom-trained model dynamically.

## Technology Stack

* **Language:** Python
* **User Interface:** PySide6
* **PDF Processing:** PyMuPDF
* **Vector Search & ML:** FAISS, sentence-transformers, PyTorch
* **Local Inference:** Ollama (running Qwen3)
* **Database:** SQLite (for managing workspaces and localized chat histories)

## Limitations

* **Synthetic Evaluation:** Training questions are LLM-generated and may occasionally be simpler than real-world user queries.
* **Scanned PDFs:** Scanned documents lacking an embedded text layer (OCR) are currently unsupported.
* **Data Dependency:** Performance gains and model accuracy scale proportionally with the overall quantity and quality of the uploaded PDFs.

## Acknowledgements

* This repository is built upon foundations from the original codebase created by [@KalmBoolean](https://github.com/KalmBoolean). 
* Original repository: [https://github.com/KalmBoolean/DocumentScraperPlusTrainer]
