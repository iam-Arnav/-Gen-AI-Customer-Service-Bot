import streamlit as st
import spacy
from langchain_helper import get_qa_chain, create_vector_db

nlp = spacy.load("en_core_sci_sm")


def extract_medical_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]


st.title(" CUSTOMER SERVICE CHATBOT 🤖")

btn = st.button("Create Knowledgebase")

if btn:
    create_vector_db()

question = st.text_input("Question: ")

if question:

    entities = extract_medical_entities(question)

    if entities:
        st.subheader("Detected Medical Entities")
        for entity, label in entities:
            st.write(f"• **{entity}** ({label})")

    chain = get_qa_chain()
    response = chain.invoke({"query": question})

    st.header("Answer")
    st.write(response["result"])