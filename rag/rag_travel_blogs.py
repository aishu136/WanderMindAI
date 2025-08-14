import os
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_db_travel")

DEFAULT_URLS = [
    "https://nomadicmatt.com/travel-blogs/",
    "https://www.thebrokebackpacker.com/category/europe/"
]

def _scrape(url: str) -> str:
    r = requests.get(url, timeout=12, headers={"User-Agent": "travel-planner/1.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    return "\n\n".join(p.get_text(" ", strip=True) for p in soup.find_all("p"))

def build_retriever_if_needed(urls=None):
    persist = CHROMA_DIR
    if os.path.exists(persist) and any(os.scandir(persist)):
        return
    urls = urls or DEFAULT_URLS
    texts = []
    for u in urls:
        try:
            txt = _scrape(u)
            texts.append((u, txt))
        except Exception:
            pass
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs, metas = [], []
    for src, t in texts:
        for chunk in splitter.split_text(t):
            docs.append(chunk)
            metas.append({"source": src})
    if not docs:
        return
    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Chroma.from_texts(docs, embedding=emb, metadatas=metas, persist_directory=persist)

def rag_query(q: str) -> str:
    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vect = Chroma(persist_directory=CHROMA_DIR, embedding_function=emb)
    docs = vect.similarity_search(q, k=5)
    tips = []
    for d in docs:
        tips.append(f"- {d.page_content[:500]} (source: {d.metadata.get('source')})")
    return "\n".join(tips)
