from vision_helper import analyze_image
from memory import *

def ask_question(image_path, question):

    image_context = get_image_context()

    if image_context is None:

        image_context = analyze_image(image_path)

        save_image_context(image_context)

    conversation = get_context()

    prompt = f"""
You are an intelligent multimodal AI assistant.

Image Analysis:
{image_context}

Conversation:
{conversation}

User Question:
{question}

Rules:

- Use the stored image analysis.
- Use previous conversation.
- Never invent facts.
- If evidence is insufficient, explain why.
- Answer naturally like a human.
"""

    from google import genai
    from dotenv import load_dotenv
    import os

    load_dotenv()

    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY")
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    answer = response.text

    add_message("User", question)
    add_message("Assistant", answer)

    return answer