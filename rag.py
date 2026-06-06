import os
from chatbot import ask_ai

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings


# ✅ STEP 1 — Load PDF
def load_pdf(file_path):
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        print("✅ Loaded docs:", len(documents))  # Debug

        return documents
    except Exception as e:
        print("❌ Error loading PDF:", e)
        return []


# ✅ STEP 2 — Chunking
def split_documents(documents):
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

        chunks = splitter.split_documents(documents)

        print("✅ Total chunks:", len(chunks))  # Debug

        return chunks
    except Exception as e:
        print("❌ Chunking error:", e)
        return []


# ✅ STEP 3 — Create vector store
def create_vectorstore(documents):
    if not documents:
        raise ValueError("❌ No documents found to create embeddings")

    try:
        embeddings = AzureOpenAIEmbeddings(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            deployment="text-embedding-3-small",
            api_version="2024-02-15-preview"
        )

        db = FAISS.from_documents(documents, embeddings)

        return db

    except Exception as e:
        print("❌ Embedding error:", e)
        raise e


# ✅ STEP 4 — Retrieve with scoring + filtering
def retrieve_documents(db, query, k=5):
    try:
        docs_with_scores = db.similarity_search_with_score(query, k=k)

        if not docs_with_scores:
            return []

        # ✅ Sort (lower score = better)
        docs_with_scores.sort(key=lambda x: x[1])

        # ✅ Filter high-quality matches
        filtered = [
            (doc, score)
            for doc, score in docs_with_scores
            if score < 0.7  # safer threshold
        ]

        print("✅ Retrieved docs:", len(filtered))  # Debug

        return filtered[:3]  # top 3

    except Exception as e:
        print("❌ Retrieval error:", e)
        return []


# ✅ STEP 5 — Generate Answer using GPT
def generate_answer(query, docs):
    try:
        context = "\n\n".join([doc.page_content for doc, _ in docs])

        if not context.strip():
            return "⚠️ No meaningful content found in document."

        prompt = f"""
You are an AI assistant.

Use ONLY the context below to answer clearly.

Context:
{context}

Question:
{query}
"""

        return ask_ai(prompt)

    except Exception as e:
        print("❌ Answer generation error:", e)
        return "⚠️ Error generating response."


# ✅ MAIN RAG PIPELINE
def rag_pipeline(file_path, query):
    if not os.path.exists(file_path):
        return "⚠️ File not found.", []

    # Step 1
    docs = load_pdf(file_path)
    if not docs:
        return "⚠️ PDF is empty or unreadable.", []

    # Step 2
    chunks = split_documents(docs)
    if not chunks:
        return "⚠️ No content extracted from PDF.", []

    # Step 3
    try:
        db = create_vectorstore(chunks)
    except Exception:
        return "⚠️ Failed to create embeddings.", []

    # Step 4
    retrieved_docs = retrieve_documents(db, query)
    if not retrieved_docs:
        return "⚠️ No relevant content found.", []

    # Step 5
    answer = generate_answer(query, retrieved_docs)

    return answer, retrieved_docs
