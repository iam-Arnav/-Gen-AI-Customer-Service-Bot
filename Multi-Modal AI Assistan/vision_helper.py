from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def analyze_image(image_path):

    image = Image.open(image_path)

    response = client.models.generate_content(

        model="gemini-2.5-flash",

        contents=[
            """
Analyze this image thoroughly.

Extract:

- People
- Objects
- Visible text
- Scene
- Activities
- Emotions
- Important details

Return a detailed factual description.

Do NOT answer any question.
""",
            image
        ],

        config=types.GenerateContentConfig(
            temperature=0.2
        )
    )

    return response.text