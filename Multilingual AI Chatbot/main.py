import streamlit as st
import os

from langchain_helper import (
    create_vector_db,
    ask_question,
)

from memory import clear_memory

st.set_page_config(
    page_title="Multilingual AI Chatbot",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Multilingual AI Chatbot")
st.caption(
    "Supports English, Hindi, Spanish, French and German while preserving conversation context."
)

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:

    st.header("Knowledge Base")

    if st.button("Create / Refresh Knowledge Base"):

        if os.path.exists("faiss_index"):
            import shutil
            shutil.rmtree("faiss_index")

        with st.spinner("Creating vector database..."):
            create_vector_db()

        st.success("Knowledge Base Ready!")

    st.divider()

    if st.button("Clear Conversation"):

        clear_memory()
        st.session_state.history = []

        st.success("Conversation Cleared")

for chat in st.session_state.history:

    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

prompt = st.chat_input(
    "Ask me anything..."
)

if prompt:

    st.session_state.history.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            answer = ask_question(prompt)

            st.markdown(answer)

    st.session_state.history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
