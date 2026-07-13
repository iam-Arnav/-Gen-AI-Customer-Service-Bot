import streamlit as st
from langchain_helper import get_qa_chain, create_vector_db
from sentiment import analyze_sentiment

st.title(" CUSTOMER SERVICE CHATBOT 🤖")

btn = st.button("Create Knowledgebase")

if btn:
    create_vector_db()

question = st.text_input("Question: ")

if question:

    sentiment = analyze_sentiment(question)

    chain = get_qa_chain()

    response = chain.invoke(
        {
            "query": question
        }
    )

    # Works with both RetrievalQA and newer chains
    answer = response.get("result", response.get("answer", ""))

    if sentiment == "😊 Positive":
        answer = (
            "😊 I'm glad to hear that!\n\n"
            + answer
        )

    elif sentiment == "😞 Negative":
        answer = (
            "😔 I'm sorry you're experiencing this. "
            "I'll do my best to help.\n\n"
            + answer
        )

    st.header("Answer")
    st.write(answer)

    st.markdown("---")
    st.subheader("Detected Sentiment")
    st.success(sentiment)