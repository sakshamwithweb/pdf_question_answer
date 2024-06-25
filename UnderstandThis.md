# Full-Stack PDF Question Answer Application

This repository contains a full-stack application developed for an internship assignment. The application allows users to upload PDF documents, ask questions related to the content of these documents, and receive answers processed using natural language processing (NLP) techniques.

## Technologies Used

- **Backend**: FastAPI (Python)
- **Frontend**: React.js (JavaScript/TypeScript)
- **Database**: SQLite
- **NLP Processing**: Eden AI (formerly ChatGPT)
- **File Storage**: Local filesystem

## Features

- **PDF Upload**: Users can upload PDF documents to the application.
- **Question Asking**: Users can ask questions regarding the content of uploaded PDFs.
- **Answering**: The system processes questions using NLP to provide answers based on PDF content.
- **User Interface**: Provides an intuitive UI for file upload, question asking, and displaying answers.

## Setup Instructions

### Backend (FastAPI)

1. Clone the repository:

   ```bash
   git clone https://github.com/sakshamwithweb/pdf_question_answer
   cd pdf_question_answer/backend
   ```

2. Install dependencies:

   ```bash
   pip install pip install fastapi pydantic uvicorn PyPDF2 requests
   ```

3. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
   - The server will start at `http://localhost:8000`.

### Frontend (React.js)

1. Navigate to the frontend directory:

   ```bash
   cd pdf_question_answer/frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```
   ```bash
   npm install axios react-toastify react-icons
   ```

3. Start the development server:
   ```bash
   npm start
   ```
   - The frontend will be available at `http://localhost:3000`.

### Configuration

- Ensure that CORS settings in the FastAPI backend (`main.py`) allow requests from your frontend URL (`http://localhost:3000` by default).

### Database

- The application uses SQLite for storing metadata about uploaded PDF documents. The database file (`pdf_metadata.db`) will be created automatically.

## API Documentation

- Detailed API documentation is available via Swagger UI at `http://localhost:8000/docs` when the FastAPI server is running.

## Demo

- I have provided a link for video

## Caution

- I don't have purchased any subscription for openai chatgpt 3.5 turbo. It is just trial. App may not work when you upload a pdf which has nuch content. Suitable for 1-4 page.

- It supports english only. Ensure pdf has only english content.