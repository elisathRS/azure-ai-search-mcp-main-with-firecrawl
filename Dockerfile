# syntax=docker/dockerfile:1.6
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    HF_HOME=/opt/hf-cache \
    NLTK_DATA=/opt/nltk_data

WORKDIR /app

# System deps kept minimal; torch wheels already bundle their own runtimes.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download models + NLTK data at build time so the MCP starts fast.
RUN python -c "import nltk; [nltk.download(p, download_dir='${NLTK_DATA}', quiet=True) for p in ('punkt','punkt_tab','stopwords')]"
RUN python -c "from sentence_transformers import SentenceTransformer, CrossEncoder; \
SentenceTransformer('all-MiniLM-L6-v2'); \
CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')"

COPY hybrid_search ./hybrid_search
COPY files_converted ./files_converted
COPY server.py ./server.py

# MCP speaks JSON-RPC over stdio; no port needs to be exposed.
CMD ["python", "-u", "server.py"]
