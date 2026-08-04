from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import os

from app.index import COLLECTION_NAME

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
K = int(os.getenv("RAG_TOP_K", "5"))


def _get_embeddings() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")


def _get_vector_store() -> QdrantVectorStore:
    return QdrantVectorStore(
        client=QdrantClient(url=QDRANT_URL),
        collection_name=COLLECTION_NAME,
        embedding=_get_embeddings(),
    )


def retrieve(query: str, k: int = K) -> list:
    vector_store = _get_vector_store()
    return vector_store.similarity_search(query, k=k)


def generate_answer(query: str, documents: list) -> str:
    context = "\n\n".join(doc.page_content for doc in documents)

    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        temperature=0.3,
    )

    prompt = f"""You are a helpful assistant that answers questions based ONLY on the provided context.
If the answer cannot be found in the context, say so clearly. Do not make up information.

Context:
{context}

Question: {query}

Answer:"""

    response = llm.invoke(prompt)
    return response.content


def rag_query(query: str, k: int = K) -> dict:
    documents = retrieve(query, k=k)
    answer = generate_answer(query, documents)
    return {
        "query": query,
        "response": answer,
        "sources": [
            {"page": doc.metadata.get("page"), "text": doc.page_content[:200]}
            for doc in documents
        ],
    }
