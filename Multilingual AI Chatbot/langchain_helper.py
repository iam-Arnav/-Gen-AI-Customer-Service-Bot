import os
import pandas as pd
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from translator import (
    translate_to_english,
    translate_from_english,
)

from language_detector import detect_language
from memory import add_message, get_context

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found.")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
)

DB_PATH = "faiss_index"


def create_vector_db():

    df = pd.read_csv("dataset.csv", encoding="cp1252")

    documents = []

    for _, row in df.iterrows():

        documents.append(
            Document(
                page_content=f"Question: {row['prompt']}\nAnswer: {row['response']}"
            )
        )

    vectordb = FAISS.from_documents(
        documents,
        embeddings,
    )

    vectordb.save_local(DB_PATH)

    print("Knowledge Base Created Successfully")


def load_vector_db():

    return FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )


def retrieve_context(question):

    db = load_vector_db()

    docs = db.similarity_search(
        question,
        k=3,
    )

    context = ""

    for doc in docs:

        context += doc.page_content + "\n\n"

    return context


def ask_question(question):

    language_code, _ = detect_language(question)

    english_question = translate_to_english(
        question,
        language_code,
    )

    history = get_context()

    context = retrieve_context(
        english_question
    )

    prompt = f"""
You are an intelligent multilingual customer service assistant.

Conversation History:

{history}

Knowledge Base:

{context}

Current User Question:

{english_question}

Instructions:

- Answer ONLY using the knowledge base.
- Preserve previous conversation.
- Handle multilingual conversations naturally.
- If the answer is unavailable, reply only:
I don't know.

Answer:
"""

    response = llm.invoke(prompt)

    answer = response.content

    final_answer = translate_from_english(
        answer,
        language_code,
    )

    add_message(
        "User",
        question,
    )

    add_message(
        "Assistant",
        final_answer,
    )

    return final_answer


if __name__ == "__main__":

    create_vector_db()

    print(
        ask_question(
            "What services do you provide?"
        )
    )