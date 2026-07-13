import os
import streamlit as st
from PIL import Image

from reasoning_engine import ask_question
from validator import validate_response, confidence_message
from memory import (
    clear_memory,
    load_memory,
    get_image_context,
    save_image_context
)

st.set_page_config(
    page_title="Multi-Modal AI Assistant",
    page_icon="🤖",
    layout="wide"
)

with st.sidebar:

    st.title("🤖 Multi-Modal AI")

    st.markdown("---")

    st.write("### Features")

    st.write("🖼 Image Understanding")
    st.write("💬 Conversational Memory")
    st.write("🧠 Contextual Reasoning")
    st.write("✅ Evidence Validation")
    st.write("📷 Image + Text Reasoning")

    st.markdown("---")

    if st.button("🗑 Clear Conversation"):

        clear_memory()

        st.success("Conversation cleared.")

st.title("🤖 Multi-Modal AI Assistant")

st.write(
    "Upload an image and ask questions about it. The assistant analyzes the image once, remembers previous conversations, and answers using evidence-based reasoning."
)

col1, col2, col3 = st.columns(3)

col1.metric("Input", "Image + Text")
col2.metric("Vision Model", "Gemini 2.5 Flash")
col3.metric("Memory", "Enabled")

st.markdown("---")

uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["jpg", "jpeg", "png"]
)

question = st.text_input(
    "Ask a question about the uploaded image"
)

if "current_image" not in st.session_state:
    st.session_state.current_image = None

left, right = st.columns([1, 1])

with left:

    if uploaded_file is not None:

        os.makedirs("uploads", exist_ok=True)

        image_path = os.path.join(
            "uploads",
            uploaded_file.name
        )

        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if st.session_state.current_image != uploaded_file.name:

            clear_memory()

            save_image_context(None)

            st.session_state.current_image = uploaded_file.name

        image = Image.open(image_path)

        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )

with right:

    if uploaded_file is not None and question.strip():

        with st.spinner("Thinking..."):

            answer = ask_question(
                image_path,
                question
            )

        confidence = validate_response(answer)

        st.subheader("Answer")

        st.write(answer)

        st.subheader("Confidence")

        if confidence == "High":

            st.success(confidence_message(confidence))

        elif confidence == "Medium":

            st.info(confidence_message(confidence))

        else:

            st.warning(confidence_message(confidence))

st.markdown("---")

st.subheader("Conversation History")

history = load_memory()

if history:

    for item in history:

        if item["role"] == "User":

            with st.chat_message("user"):

                st.write(item["message"])

        else:

            with st.chat_message("assistant"):

                st.write(item["message"])

else:

    st.info("No conversation yet.")

st.markdown("---")

st.caption(
    "Multi-Modal AI Assistant built using Streamlit, Google Gemini 2.5 Flash and Python."
)