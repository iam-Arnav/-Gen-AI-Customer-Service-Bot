import json
import os

MEMORY_FILE = "conversation/history.json"

IMAGE_CONTEXT = None


def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(memory):

    os.makedirs("conversation", exist_ok=True)

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)


def add_message(role, message):

    memory = load_memory()

    memory.append({
        "role": role,
        "message": message
    })

    save_memory(memory)


def get_context(last_n=8):

    memory = load_memory()

    text = ""

    for item in memory[-last_n:]:

        text += f"{item['role']}: {item['message']}\n"

    return text


def clear_memory():

    global IMAGE_CONTEXT

    IMAGE_CONTEXT = None

    save_memory([])


def save_image_context(context):

    global IMAGE_CONTEXT
    
    IMAGE_CONTEXT = context


def get_image_context():

    return IMAGE_CONTEXT