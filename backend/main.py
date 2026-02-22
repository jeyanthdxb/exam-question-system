import os
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parent.parent 
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY not found. Make sure .env is in project root.")

client = OpenAI(api_key=api_key)


app = FastAPI(title="Exam Question System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


OUTPUT_JSON_DIR = BASE_DIR / "backend" / "output_json"
IMAGE_DIR = BASE_DIR / "backend" / "extracted_images"

IMAGE_DIR.mkdir(parents=True, exist_ok=True)

app.mount(
    "/extracted_images",
    StaticFiles(directory=str(IMAGE_DIR)),
    name="images"
)


class ChatRequest(BaseModel):
    question: str
    message: str


class Question(BaseModel):
    question_number: int
    subject: str
    question_text: str
    options: List[str]
    images: List[str]
    image_options: List[str]



@app.get("/")
def root():
    return {"status": "Backend running successfully"}


@app.get("/papers")
def get_papers():
    if not OUTPUT_JSON_DIR.exists():
        raise HTTPException(status_code=404, detail="output_json folder not found")

    return [
        file.name for file in OUTPUT_JSON_DIR.iterdir()
        if file.suffix == ".json"
    ]


@app.get("/questions/{paper_name}")
def get_questions(paper_name: str):
    file_path = OUTPUT_JSON_DIR / paper_name

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Paper not found")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for q in data:
        Question(**q)

    return data


@app.post("/chat")
def chat(payload: ChatRequest):

    system_prompt = f"""
    You are an expert NEET/JEE tutor.

    - Do NOT directly give the final answer.
    - Explain step-by-step.
    - Use Socratic questioning.
    - Guide logically.

    Question:
    {payload.question}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": payload.message}
        ],
        temperature=0.7
    )

    return {"reply": response.choices[0].message.content}