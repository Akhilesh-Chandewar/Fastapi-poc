from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

load_dotenv()

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "learning_rag_gemini")

PDF_FILE = os.getenv("PDF_FILE", "Akhilesh_Chandewar_Resume_2026.pdf")


def get_embedding_model() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")


def load_and_chunk_pdf(pdf_path: Path, chunk_size: int = 1000, chunk_overlap: int = 400) -> list:
    loader = PyPDFLoader(file_path=str(pdf_path))
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return text_splitter.split_documents(docs)


def index_documents(pdf_path: Path | None = None, qdrant_url: str | None = None) -> int:
    pdf_path = pdf_path or DATA_DIR / PDF_FILE
    qdrant_url = qdrant_url or os.getenv("QDRANT_URL")

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    chunks = load_and_chunk_pdf(pdf_path)

    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=get_embedding_model(),
        url=qdrant_url,
        collection_name=COLLECTION_NAME,
    )
    return len(chunks)


if __name__ == "__main__":
    count = index_documents()
    print(f"Indexing of documents done with Gemini: {count} chunks stored in '{COLLECTION_NAME}'.")
