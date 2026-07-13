import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from langchain_helper import create_vector_db

KNOWLEDGE_FOLDER = "knowledge"


class KnowledgeHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        print(f"\nNew file detected: {event.src_path}")

        time.sleep(2)

        try:
            create_vector_db()
            print("Knowledge Base Updated Successfully!\n")

        except Exception as e:
            print(f"Error updating knowledge base: {e}")


if __name__ == "__main__":

    event_handler = KnowledgeHandler()

    observer = Observer()

    observer.schedule(
        event_handler,
        KNOWLEDGE_FOLDER,
        recursive=False
    )

    observer.start()

    print("Watching knowledge folder...")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()