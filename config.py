# Central settings shared by learner.py, pairgen.py, finetune.py and evaluate.py

# Embedding model. After fine-tuning, change this to "models/bge-finetuned"
# and REBUILD the index (Index Folder), because vectors from different models
# are not compatible.
EMBED_MODEL = "models/bge-finetuned"

# bge models work best when queries (not documents) get this prefix.
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

# Reranker (cross-encoder) applied to the top candidates from FAISS.
USE_RERANKER = True
RERANK_MODEL = "BAAI/bge-reranker-base"
RERANK_CANDIDATES = 20

# Local LLM used to generate training questions (needs `ollama pull qwen3:8b`).
LLM_MODEL = "qwen3:8b"

# Chunking (keep identical everywhere so training chunks == indexed chunks).
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
MIN_CHUNK_CHARS = 200   # for training data; very short chunks make bad questions

# Output locations
DATA_DIR = "dl_data"
FINETUNED_DIR = "models/bge-finetuned"
