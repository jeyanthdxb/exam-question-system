README.md
# Exam Question System (JEE / NEET)

A full-stack web application that extracts structured questions from previous-year JEE/NEET PDF papers and provides an interactive question-solving interface with AI-powered Socratic tutoring.

---

## Features

- Extracts structured questions from JEE/NEET PDF papers
- Supports multiple papers (dynamic switching)
- Extracts and serves embedded images
- Structured JSON schema for each question
- React-based interactive frontend
- Per-question AI Socratic tutor (OpenAI integration)
- Backend validation tests
- Clean REST API architecture

---

##  Project Architecture


exam-system/
│
├── backend/
│ ├── papers/ # Input PDFs
│ ├── output_json/ # Extracted structured questions
│ ├── extracted_images/ # Extracted images
│ ├── extractor.py # PDF → JSON pipeline
│ ├── main.py # FastAPI backend
│ ├── validator.py # Schema validation
│ └── tests/
│
├── frontend/
│ ├── src/
│ ├── package.json
│ └── vite.config.js
│
└── README.md


---

## JSON Question Schema

Each question is structured as:

```json
{
  "question_number": 1,
  "subject": "Physics",
  "question_text": "Question text here...",
  "options": ["A", "B", "C", "D"],
  "images": ["paper_name/page1_img1.png"],
  "image_options": []
}
Extraction Pipeline

Uses PyMuPDF for text + image extraction

Regex-based structured question parsing

Supports JEE Advanced format (Q.1, Q.2, etc.)

Stores output in structured JSON format

Images saved in paper-specific folders

Run extraction:


cd backend
python extractor.py jee_2021.pdf

 Backend Setup
 Create Virtual Environment (Optional but recommended)

cd backend
python -m venv venv
venv\Scripts\activate

 Install Dependencies

pip install -r requirements.txt


If requirements.txt not present:


pip install fastapi uvicorn pymupdf python-dotenv openai

 Add OpenAI API Key

Create .env inside backend:


OPENAI_API_KEY=your_api_key_here

 Run Backend

uvicorn main:app --reload


Backend runs at:


http://127.0.0.1:8000


Swagger docs:


http://127.0.0.1:8000/docs

 Frontend Setup
 Install Dependencies

cd frontend
npm install
npm install axios

 Run Frontend

npm run dev


Frontend runs at:


http://localhost:5173

 API Endpoints
Method	Endpoint	Description
GET	/papers	List available papers
GET	/questions/{paper}	Get structured questions
POST	/chat	AI Socratic tutor response
GET	/extracted_images/{path}	Serve extracted images
 Running Tests

cd backend
pytest


Validation ensures:

Required schema fields exist

Options properly formatted

No missing keys

 AI Tutor

Each question includes a Socratic tutor powered by OpenAI.

Context-aware responses

Does not directly reveal answers

Encourages guided reasoning

 Supported Papers

JEE Advanced 2021

(Add additional NEET/JEE papers here)

The system dynamically loads all JSON files inside output_json/.

 Important Notes

.env is not committed to GitHub

node_modules/ and extracted images are ignored

Images are served statically via FastAPI

 Design Decisions

FastAPI chosen for clean REST architecture

React + Vite for lightweight frontend

Structured JSON schema for flexibility

Modular extraction pipeline

Separated backend/frontend for scalability

 Author

Jeyanth Inbakumar
Full-Stack Developer | AI Enthusiast

 Future Improvements

OCR support for scanned PDFs

Automatic subject classification

Performance optimization for large papers

Deployment to cloud (Render / Vercel / AWS)


---

