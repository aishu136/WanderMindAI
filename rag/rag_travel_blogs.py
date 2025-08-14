import os
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Directory to store Chroma vector database
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_db_travel")

# Default travel blog URLs
DEFAULT_URLS = [
    "https://nomadicmatt.com/travel-blogs/",
    "https://www.thebrokebackpacker.com/category/europe/"
]

# Load Flan-T5 locally
MODEL_NAME = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def _scrape(url: str) -> str:
    try:
        r = requests.get(url, timeout=12, headers={"User-Agent": "travel-planner/1.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        return "\n\n".join(p.get_text(" ", strip=True) for p in soup.find_all("p"))
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return ""

def build_retriever_if_needed(urls=None):
    persist = CHROMA_DIR
    if os.path.exists(persist) and any(os.scandir(persist)):
        return

    urls = urls or DEFAULT_URLS
    texts = []
    for u in urls:
        txt = _scrape(u)
        if txt:
            texts.append((u, txt))

    if not texts:
        print("No texts retrieved for RAG.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs, metas = [], []
    for src, t in texts:
        for chunk in splitter.split_text(t):
            docs.append(chunk)
            metas.append({"source": src})

    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Chroma.from_texts(docs, embedding=emb, metadatas=metas, persist_directory=persist)
    print(f"Chroma vector store built with {len(docs)} chunks.")

def generate_itinerary(prompt: str) -> str:
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
    outputs = model.generate(**inputs, max_length=1024, do_sample=True, temperature=0.7)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def rag_query(query: str) -> str:
    # Load vector store
    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vect = Chroma(persist_directory=CHROMA_DIR, embedding_function=emb)

    # Retrieve relevant chunks
    docs = vect.similarity_search(query, k=8)
    context = "\n\n".join(d.page_content for d in docs)

    # Prepare prompt
    prompt = PromptTemplate(
        template=(
            "You are a professional travel planner.\n"
            "User request: {query}\n\n"
            "Here are some travel blog excerpts:\n{context}\n\n"
            "Based on these, create a detailed travel itinerary including:\n"
            "- Day-by-day breakdown\n"
            "- Activities and attractions\n"
            "- Food recommendations\n"
            "- Local tips\n"
            "- Estimated costs where possible\n"
            "Make it structured and easy to read."
        ),
        input_variables=["query", "context"]
    )

    full_prompt = prompt.format(query=query, context=context)
    itinerary = generate_itinerary(full_prompt)
    return itinerary
