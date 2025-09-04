import json
import os


def record_text(text: str, file_name: str) -> None:
    with open(f'Records\\{file_name}.txt', 'w') as text_file:
        text_file.write(text)
        text_file.close()


def push_json(dictionary: dict):
    DATA_FILE = "storage.json"

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

