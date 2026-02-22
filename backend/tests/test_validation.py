import os
import json
from backend.validator import validate_questions

def test_validation():
    base_dir = os.path.dirname(os.path.dirname(__file__)) 
    file_path = os.path.join(base_dir, "output_json", "neet_2023.json")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    validate_questions(data)