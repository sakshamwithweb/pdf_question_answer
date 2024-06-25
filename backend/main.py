from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os
from datetime import datetime
from PyPDF2 import PdfReader
import requests

app = FastAPI()

# Allow CORS for the frontend application
origins = [
    "http://localhost:3000",  # Adjust to your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to extract text from uploaded PDF file
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to retrieve full content of PDF based on filename
def get_full_content(filename):
    conn = sqlite3.connect('pdf_metadata.db')
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM pdf_metadata WHERE filename=?', (filename,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]  # Return full content as a string
    else:
        return None

# Upload PDF endpoint
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    file_location = f"pdf_files/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    text_content = extract_text_from_pdf(file_location)

    # Store metadata in SQLite database
    conn = sqlite3.connect('pdf_metadata.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pdf_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            upload_date TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        INSERT INTO pdf_metadata (filename, upload_date, content) 
        VALUES (?, ?, ?)
    ''', (file.filename, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text_content))
    conn.commit()
    conn.close()

    return {"filename": file.filename, "content": text_content[:200]}  # Return first 200 chars for brevity

# Model for question request
class QuestionRequest(BaseModel):
    filename: str
    question: str

# Function to ask question using ChatGPT
def ask_question_with_chatgpt(question, contentOfPDF):
    # Ensure previous_history includes the content of the book
    if not contentOfPDF:
        raise ValueError("The content of pdf must include.")

    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYThlZDlhMmItYmFkNi00NTA4LTlkN2EtZDFmNWM0OTgyMzQ2IiwidHlwZSI6ImFwaV90b2tlbiJ9.zA-e5C-qgw36rLHk1FdTtGWyaoYesAH27_izlxeTzuc" 
    }
    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers": "openai",
        "text": f"{contentOfPDF}\nabove content is a content of pdf. I have to ask a question related to that-\nQ:-{question}",
        "chatbot_global_action": "Act as an assistant. Give only main response",
        "previous_history": [],
        "temperature": 0.0,
        "max_tokens": 1500,
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        if 'openai' in result and 'generated_text' in result['openai']:
            return result['openai']['generated_text']
        else:
            raise ValueError("Unexpected API response format")
    except requests.exceptions.RequestException as e:
        print(f"Request to ChatGPT API failed: {e}")
        raise
    except (KeyError, ValueError) as e:
        print(f"Error processing API response: {e}")
        raise

# Endpoint to ask a question about the PDF content
@app.post("/ask-question/")
async def ask_question(request: QuestionRequest):
    # Get full content of the PDF file
    content = get_full_content(request.filename)
    if not content:
        raise HTTPException(status_code=404, detail="File not found")

    # Use ChatGPT to answer the question based on the content
    answer = ask_question_with_chatgpt(request.question, content)
    return {"answer": answer}

# Ensure the directory exists for PDF uploads
os.makedirs("pdf_files", exist_ok=True)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
