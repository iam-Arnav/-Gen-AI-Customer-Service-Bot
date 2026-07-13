import os
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

DB_FAISS_PATH = "faiss_index"




llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
)



embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)




def create_vector_db():

    loader = CSVLoader(
        file_path="medical_dataset.csv",
        encoding="utf-8"
    )

    documents = loader.load()

    vectordb = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )

    vectordb.save_local(DB_FAISS_PATH)

    print("Medical Knowledge Base Created Successfully!")




def get_qa_chain():

    vectordb = FAISS.load_local(
        DB_FAISS_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = vectordb.as_retriever(
        search_kwargs={"k": 5}
    )

    prompt_template = """
You are an intelligent Medical Question Answering Assistant.

Answer ONLY using the provided medical context.

Rules:

1. Never make up medical information.

2. Never diagnose diseases.

3. Never prescribe medicines.

4. If the answer is not found in the context,
reply exactly:

I don't know.

Context:
{context}

Question:
{question}

Answer:
"""

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": PROMPT
        }
    )

    return chain


if __name__ == "__main__":

    create_vector_db()

    chain = get_qa_chain()

    response = chain.invoke(
        {
            "query": "What is leukemia?"
        }
    )

    print(response["result"])