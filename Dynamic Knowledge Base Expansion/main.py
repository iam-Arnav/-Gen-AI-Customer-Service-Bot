import os
import shutil
import streamlit as st

from langchain_helper import (
    create_vector_db,
    get_qa_chain,
)

KNOWLEDGE_FOLDER = "knowledge"

if not os.path.exists(KNOWLEDGE_FOLDER):
    os.makedirs(KNOWLEDGE_FOLDER)

st.title(" CUSTOMER SERVICE CHATBOT 🤖")

uploaded_file = st.file_uploader(
    "Upload Knowledge File",
    type=["pdf", "txt", "csv"]
)

if uploaded_file:

    save_path = os.path.join(
        KNOWLEDGE_FOLDER,
        uploaded_file.name
    )

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"{uploaded_file.name} uploaded successfully!")

    create_vector_db()

    st.success("Knowledge Base Updated Successfully!")

st.subheader("Knowledge Sources")

files = os.listdir(KNOWLEDGE_FOLDER)

if files:
    for file in files:
        st.write(f"• {file}")
else:
    st.info("No knowledge files uploaded.")

question = st.text_input("Question: ")

if question:

    chain = get_qa_chain()

    response = chain.invoke(
        {
            "query": question
        }
    )

    st.header("Answer")

    st.write(response["result"])