import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "data.json")


def load_data():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"users": [], "products": []}, f)

    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)
