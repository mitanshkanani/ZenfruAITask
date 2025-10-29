# backend/utils/file_utils.py
import json
from pathlib import Path


def read_json_file(file_path: str):
    """
    Reads a JSON file and returns the data.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json_file(file_path: str, data):
    """
    Writes data to a JSON file.
    """
    path = Path(file_path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
