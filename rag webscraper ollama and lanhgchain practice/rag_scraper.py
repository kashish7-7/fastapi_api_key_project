import sys
from typing import List
import os

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from bs4 import SoupStrainer

PERSIST_DIR = "chroma_db"
LLM_MODEL   = "llama3.1"
EMBED_MODEL = "nomic-embed-text"

def ensure_user_agent():
    if not os.environ.get("USER_AGENT"):
        os.environ["USER_AGENT"] = "Mozilla/5.0 (RAG-Scraper/1.0)"

def scrape_urls(urls: List[str]):
    strainer = SoupStrainer(class_=("content", "content-area", "post-content", "article", "entry-content"))
    loader = WebBaseLoader(web_paths=urls, bs_kwargs={"parse_only": strainer})
    docs = loader.load()
    print(f"Fetched {len(docs)} document(s).")
    return docs

def chunk_docs(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(docs)
    print(f"Created {len(chunks)} chunk(s).")
    return chunks

def build_or_update_vectorstore(chunks):
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    try:
        vs = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
        vs.add_documents(chunks)
    except Exception:
        vs = Chroma.from_documents(chunks, embeddings, persist_directory=PERSIST_DIR)
    vs.persist()
    print(f"Vector store stored in: {PERSIST_DIR}")
    return vs

def make_qa_chain(vs):
    retriever = vs.as_retriever(search_kwargs={"k": 4})
    llm = ChatOllama(model=LLM_MODEL, temperature=0.2)
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

def interactive_chat(chain):
    print("\nAsk questions. Type 'exit' to quit.")
    while True:
        q = input("\nQ: ").strip()
        if q.lower() in ["exit", "quit"]:
            break
        res = chain({"query": q})
        print("\nA:", res["result"])

def main():
    if len(sys.argv) < 2:
        print("Usage: python rag_scraper.py <url1> [<url2>...]")
        return

    ensure_user_agent()
    urls = sys.argv[1:]
    docs = scrape_urls(urls)
    chunks = chunk_docs(docs)
    vs = build_or_update_vectorstore(chunks)
    chain = make_qa_chain(vs)
    interactive_chat(chain)

if __name__ == "__main__":
    main()
