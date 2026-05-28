from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings


def load_pdf(file):
    loader = PyPDFLoader(file)
    documents = loader.load()
    return documents


def create_vectorstore(documents):
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(documents, embeddings)
    return db


def query_pdf(db, query):
    docs = db.similarity_search(query)
    return docs[0].page_content
