import streamlit as st
from langchain_helper import ask_question
from paper_search import search_papers
from concept_visualizer import get_concept_tree

st.set_page_config(
    page_title="ArXiv Research Assistant",
    page_icon="📚",
    layout="wide"
)

with st.sidebar:

    st.title("📚 ArXiv Research Assistant")

    st.markdown("---")

    st.write("### Features")

    st.write("💬 Research Chat")
    st.write("📄 Paper Search")
    st.write("📝 Paper Summarizer")
    st.write("🧠 Concept Visualizer")

    st.markdown("---")

    st.caption("Powered by Ollama + FAISS + LangChain")

st.title("📚 ArXiv Research Assistant")

col1, col2, col3 = st.columns(3)

col1.metric("Research Papers", "20,000")
col2.metric("LLM", "Phi3 Mini")
col3.metric("Vector DB", "FAISS")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(
    [
        "💬 Research Chat",
        "📄 Search Papers",
        "🧠 Concept Visualizer"
    ]
)

with tab1:

    question = st.text_area(
        "Ask a Computer Science research question",
        height=150
    )

    if st.button("Ask Expert"):

        if question.strip():

            with st.spinner("Searching research papers..."):

                answer = ask_question(question)

            st.subheader("Answer")

            st.write(answer)

        else:

            st.warning("Please enter a question.")

with tab2:

    keyword = st.text_input("Search research papers")

    if keyword:

        papers = search_papers(keyword)

        if len(papers) == 0:

            st.warning("No papers found.")

        else:

            st.success(f"{len(papers)} paper(s) found")

            for _, row in papers.iterrows():

                with st.expander(f"📄 {row['title']}"):

                    st.write(row["content"][:1200] + "...")

                    if st.button(
                        "Summarize Paper",
                        key=f"summary_{row['title']}"
                    ):

                        with st.spinner("Generating summary..."):

                            summary = ask_question(
                                f"Summarize the following research paper:\n\n{row['content']}"
                            )

                        st.success(summary)

with tab3:

    concept = st.text_input(
        "Enter a Computer Science concept",
        key="concept"
    )

    if concept:

        tree = get_concept_tree(concept)

        if tree is None:

            with st.spinner("Generating explanation..."):

                explanation = ask_question(
                    f"Explain the concept '{concept}' with examples."
                )

            st.write(explanation)

        else:

            st.success(concept.title())

            for parent, children in tree.items():

                st.markdown(f"### {parent}")

                for child in children:

                    st.markdown(f"- {child}")

st.markdown("---")

st.caption(
    "Computer Science Research Assistant built using Streamlit, FAISS, Ollama, HuggingFace Embeddings and LangChain."
)