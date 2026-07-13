from dotenv import load_dotenv

from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM

load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

FAISS_PATH = "faiss_index"


def create_vector_db():

    loader = CSVLoader(
        file_path="knowledge/cs_arxiv.csv",
        encoding="utf-8"
    )

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = splitter.split_documents(documents)

    db = FAISS.from_documents(
        docs,
        embeddings
    )

    db.save_local(FAISS_PATH)

    print("FAISS index created successfully!")


def load_vector_db():

    return FAISS.load_local(
        FAISS_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


llm = OllamaLLM(
    model="phi3:mini"
)


def ask_question(question):

    db = load_vector_db()

    retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 6,
            "fetch_k": 20
        }
    )

    docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are an expert Computer Science research assistant.

Answer ONLY from the retrieved research papers.

If the papers do not contain enough information,
say that instead of making up an answer.

Research Papers:
{context}

Question:
{question}

Format your response as:

Direct Answer

Detailed Explanation

Key Concepts

Practical Applications

Summary
"""

    return llm.invoke(prompt)


if __name__ == "__main__":
    create_vector_db()