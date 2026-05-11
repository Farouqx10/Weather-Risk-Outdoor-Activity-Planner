import json
import os
from datetime import datetime
import re

DATA_FILE = "data/history.json"

def save_search(entry):
    if not os.path.exists("data"):
        os.makedirs("data")

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_history():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
            return []

def create_entry(location, activity, risk):
    return {
        "location": location,
        "activity": activity,
        "risk": risk,
        "time": datetime.now().strftime("%D-%m-%y %H:%M:%S")
    }

FAV_FILE = "data/favourites.json"

def save_favourite(location):
    if not os.path.exists("data"):
        os.makedirs("data")

    try:
        with open(FAV_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    if location not in data:
        data.append(location)

    with open(FAV_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_favourites():
    try:
        with open(FAV_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def clean_location(location):
    location = location.strip()
    pattern = r"^[A-Za-z\s,-]+$"

    if re.match(pattern, location):
        return location.title()

    raise ValueError("Invalid location name")