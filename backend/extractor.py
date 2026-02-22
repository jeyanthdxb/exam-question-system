import os
import re
import json
import fitz  
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PAPERS_DIR = BASE_DIR / "papers"
OUTPUT_JSON_DIR = BASE_DIR / "output_json"
IMAGES_DIR = BASE_DIR / "extracted_images"

OUTPUT_JSON_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)


def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        full_text += page.get_text() + "\n"

    return full_text



def extract_questions(full_text):
    questions = []

    pattern = r"(?:\n|^)Q\.(\d{1,3})\s"
    splits = re.split(pattern, full_text)


    for i in range(1, len(splits), 2):
        q_no = splits[i]
        block = splits[i + 1]

        options = re.findall(r"\([A-D]\)\s*(.*)", block)

        question_text = re.sub(r"\([A-D]\)\s*.*", "", block).strip()

        questions.append({
            "question_number": int(q_no),
            "subject": "General",
            "question_text": question_text,
            "options": options,
            "images": [],
            "image_options": []
        })

    return questions



def extract_images(pdf_path, paper_name):
    doc = fitz.open(pdf_path)
    paper_image_dir = IMAGES_DIR / paper_name
    paper_image_dir.mkdir(exist_ok=True)

    for page_index in range(len(doc)):
        page = doc[page_index]
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            image_filename = f"page{page_index+1}_img{img_index+1}.png"
            image_path = paper_image_dir / image_filename

            with open(image_path, "wb") as f:
                f.write(image_bytes)



def process_pdf(pdf_filename):
    pdf_path = PAPERS_DIR / pdf_filename

    if not pdf_path.exists():
        print("❌ PDF not found.")
        return

    print(f"Processing: {pdf_filename}")

    full_text = extract_text(pdf_path)

    if len(full_text.strip()) == 0:
        print("⚠ This PDF appears to be scanned (no extractable text).")
        return

    questions = extract_questions(full_text)

    print("Questions detected:", len(questions))

    paper_name = pdf_filename.replace(".pdf", "")
    extract_images(pdf_path, paper_name)

    output_file = OUTPUT_JSON_DIR / f"{paper_name}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=4)

    print(f"Saved JSON to {output_file}")


if __name__ == "__main__":
    if len(os.sys.argv) < 2:
        print("Usage: python extractor.py <pdf_filename>")
    else:
        process_pdf(os.sys.argv[1])