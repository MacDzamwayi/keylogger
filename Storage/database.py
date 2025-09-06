import json
import os
import time
import threading


class Recorder:
    def __init__(self, file_name: str):
        module_dir = os.path.join(os.path.dirname(__file__), "Records")
        os.makedirs(module_dir, exist_ok=True)

        current_time = time.strftime("%H-%M-%S")
        self.data_file = os.path.join(module_dir, f"{file_name}_{current_time}.txt")

        self.recording = False
        self.thread = None

    def start(self, text_source):
        """
        text_source: function or callable that returns the next text string
        """
        if self.recording:
            return  # already running

        self.recording = True
        self.thread = threading.Thread(target=self._run, args=(text_source,), daemon=True)
        self.thread.start()

    def stop(self):
        """Stop recording gracefully."""
        self.recording = False
        if self.thread:
            self.thread.join(timeout=1)

    def _run(self, text_source):
        """Internal loop that writes text continuously."""
        with open(self.data_file, 'a', encoding="utf-8") as f:
            while self.recording:
                text = text_source()  # ask for new text
                if text:
                    f.write(text + "\n")
                    f.flush()
                time.sleep(0.5)  # adjust polling speed


def delete_json(key: str):
    module_dir = os.path.dirname(__file__)
    DATA_FILE = os.path.join(module_dir, "storage.json")

    with open(DATA_FILE, 'r+') as db_file:
        storage = json.load(db_file)
        del storage[key]
        db_file.seek(0)
        json.dump(storage, db_file, indent=4)
        db_file.truncate()


def push_json(dictionary: dict):
    module_dir = os.path.dirname(__file__)
    DATA_FILE = os.path.join(module_dir, "storage.json")

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as data:
            json.dump({}, data)

    with open(DATA_FILE, 'r+') as db_file:
        storage = json.load(db_file)
        storage.update(dictionary)
        db_file.seek(0)
        json.dump(storage, db_file, indent=4)
        db_file.truncate()


def pull_json() -> dict:
    module_dir = os.path.dirname(__file__)
    DATA_FILE = os.path.join(module_dir, "storage.json")

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as data:
            json.dump({}, data)

    with open(DATA_FILE, 'r+') as db_file:
        storage = json.load(db_file)
        return storage
