import os

def validate_questions(data):
    numbers = set()

    for q in data:
        assert q["question_number"] not in numbers
        numbers.add(q["question_number"])

        assert len(q["options"]) >= 4
        assert q["question_text"] != ""

        for img in q["images"]:
            assert os.path.exists(f"extracted_images/{img}")