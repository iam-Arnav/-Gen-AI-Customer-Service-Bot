import os
from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)

from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import RetrievalQA
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.1,
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GOOGLE_API_KEY,
)

vectordb_file_path = "faiss_index"


def create_vector_db():
    loader = CSVLoader(
        file_path="dataset.csv",
        source_column="prompt"
    )

    data = loader.load()

    vectordb = FAISS.from_documents(
        documents=data,
        embedding=embeddings,
    )

    vectordb.save_local(vectordb_file_path)

    print("Vector DB created successfully.")


def get_qa_chain():

    vectordb = FAISS.load_local(
        vectordb_file_path,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    retriever = vectordb.as_retriever(
        search_kwargs={"k": 3}
    )

    prompt_template = """
Given the following context and a question, answer ONLY from the provided context.

If the answer is not present, simply say:

"I don't know."

Context:
{context}

Question:
{question}

Answer:
"""

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"],
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": PROMPT
        },
    )

    return chain


if __name__ == "__main__":
    create_vector_db()

    chain = get_qa_chain()

    response = chain.invoke(
        {"query": "Hello"}
    )

    print(response["result"])