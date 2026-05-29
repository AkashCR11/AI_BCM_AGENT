from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from chatbot import ask_ai
import os

# ✅ STEP 1 — Load PDF
def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents


# ✅ STEP 2 — Chunking (VERY IMPORTANT)
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    return splitter.split_documents(documents)


# ✅ STEP 3 — Create vector store
def create_vectorstore(documents):
    embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    deployment="text-embedding-3-small",  # ✅ create this in Azure if not present
    api_version="2024-02-15-preview"
)

    db = FAISS.from_documents(documents, embeddings)

    return db


# ✅ STEP 4 — Retrieve with scoring + reranking
def retrieve_documents(db, query, k=5):
    docs_with_scores = db.similarity_search_with_score(query, k=k)

    # ✅ Sort by score (lower = better)
    docs_with_scores.sort(key=lambda x: x[1])

    # ✅ Filter (remove bad matches)
    filtered = [
        (doc, score)
        for doc, score in docs_with_scores
        if score < 0.5
    ]

    return filtered[:3]  # top 3 docs


# ✅ STEP 5 — Generate answer using GPT
def generate_answer(query, docs):
    context = "\n\n".join([doc.page_content for doc, _ in docs])

    prompt = f"""
You are a helpful AI assistant.

Use ONLY the context below to answer.

Context:
{context}

Question:
{query}
"""

    return ask_ai(prompt)


# ✅ MAIN RAG FUNCTION
def rag_pipeline(file_path, query):
    docs = load_pdf(file_path)
    chunks = split_documents(docs)

    db = create_vectorstore(chunks)

    retrieved_docs = retrieve_documents(db, query)

    answer = generate_answer(query, retrieved_docs)

    return answer, retrieved_docs
