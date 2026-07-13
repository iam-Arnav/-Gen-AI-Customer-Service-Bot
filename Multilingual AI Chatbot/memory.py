import json
import os

MEMORY_FILE = "memory.json"


def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(memory):

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

    context = ""

    for msg in memory[-last_n:]:

        context += f"{msg['role']}: {msg['message']}\n"

    return context


def clear_memory():

    save_memory([])