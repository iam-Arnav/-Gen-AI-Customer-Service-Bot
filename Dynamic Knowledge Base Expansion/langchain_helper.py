import os
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_community.document_loaders import (
    CSVLoader,
    TextLoader,
    PyPDFLoader,
)

from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

KNOWLEDGE_FOLDER = "knowledge"
FAISS_PATH = "faiss_index"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def load_documents():

    documents = []

    os.makedirs(KNOWLEDGE_FOLDER, exist_ok=True)

    for file in os.listdir(KNOWLEDGE_FOLDER):

        path = os.path.join(KNOWLEDGE_FOLDER, file)

        try:

            if file.lower().endswith(".pdf"):
                loader = PyPDFLoader(path)

            elif file.lower().endswith(".txt"):
                loader = TextLoader(path, encoding="utf-8")

            elif file.lower().endswith(".csv"):
                loader = CSVLoader(path, encoding="utf-8")

            else:
                continue

            documents.extend(loader.load())

        except Exception as e:
            print(f"Skipping {file}: {e}")

    return documents


def create_vector_db():

    documents = load_documents()

    if len(documents) == 0:
        print("No documents found.")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    if len(chunks) == 0:
        print("No text chunks created.")
        return

    vectordb = FAISS.from_documents(
        chunks,
        embeddings
    )

    vectordb.save_local(FAISS_PATH)

    print("Knowledge Base Updated Successfully!")


def get_qa_chain():

    vectordb = FAISS.load_local(
        FAISS_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    retriever = vectordb.as_retriever(
        search_kwargs={"k": 5}
    )

    prompt_template = """
You are an intelligent AI Assistant.

Answer ONLY using the supplied context.

If the answer is not available in the context, reply exactly:

I don't know.

Context:
{context}

Question:
{question}

Answer:
"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"],
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": prompt
        },
    )

    return chain


if __name__ == "__main__":
    create_vector_db()