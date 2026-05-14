import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "knowledge")
DB_DIR = os.path.join(os.path.dirname(__file__), "data", "chroma_db")

_model = None
_collection = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    return _model


def _get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=DB_DIR, settings=Settings(anonymized_telemetry=False))
        _collection = client.get_or_create_collection(name="fitness_knowledge")
    return _collection


def _load_documents():
    docs = []
    if not os.path.exists(DATA_DIR):
        return docs
    for filename in sorted(os.listdir(DATA_DIR)):
        if filename.endswith(".txt"):
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read().strip()
                if text:
                    docs.append((filename, text))
    return docs


def _chunk_text(text, max_chars=800):
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(current) + len(para) < max_chars:
            current = (current + "\n\n" + para).strip()
        else:
            if current:
                chunks.append(current)
            current = para
    if current:
        chunks.append(current)
    return chunks


def build_index(force=False):
    collection = _get_collection()
    if collection.count() > 0 and not force:
        return collection.count()

    docs = _load_documents()
    if not docs:
        return 0

    model = _get_model()
    all_chunks = []
    all_embeddings = []
    all_ids = []
    all_metas = []

    for filename, text in docs:
        chunks = _chunk_text(text)
        for i, chunk in enumerate(chunks):
            chunk_id = f"{filename}_{i}"
            all_ids.append(chunk_id)
            all_chunks.append(chunk)
            all_metas.append({"source": filename})

    all_embeddings = model.encode(all_chunks, show_progress_bar=True).tolist()

    collection.upsert(
        ids=all_ids,
        embeddings=all_embeddings,
        documents=all_chunks,
        metadatas=all_metas,
    )
    return len(all_chunks)


def retrieve(query, top_k=4):
    collection = _get_collection()
    if collection.count() == 0:
        build_index()

    model = _get_model()
    query_embedding = model.encode([query]).tolist()

    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    return results["documents"][0] if results["documents"] else []


def retrieve_as_context(query, top_k=4):
    chunks = retrieve(query, top_k)
    if not chunks:
        return "暂无相关知识库信息。"
    return "\n\n---\n\n".join(chunks)
