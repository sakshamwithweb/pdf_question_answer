import React, { useEffect, useState } from "react";
import axios from "axios";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [fileSelected, setFileSelected] = useState(false);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);

  const handleFileChange = async (event) => {
    const selectedFile = event.target.files[0];
    if (!selectedFile) return;

    if (selectedFile.type !== "application/pdf") {
      alert("Please select a PDF file.");
      return;
    }

    setFile(selectedFile);
    setFileSelected(true);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/upload-pdf/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setUploadStatus("File uploaded successfully");
      console.log(response.data);
    } catch (error) {
      setUploadStatus("File upload failed");
      console.error(error);
    }
  };

  const handleAskQuestion = async () => {
    if (!file || !question || !fileSelected) {
      toast.error(
        "Please upload a PDF file and enter and question."
      );
      return;
    }

    setMessages((prevMessages) => [
      ...prevMessages,
      { type: "user", text: question.trim() }, // Trim the question before adding
    ]);

    try {
      const response = await axios.post("http://127.0.0.1:8000/ask-question/", {
        filename: file.name,
        question: question.trim(), // Trim the question before sending
      });

      setMessages((prevMessages) => [
        ...prevMessages,
        { type: "ai", text: response.data.answer },
      ]);

      setQuestion("");
    } catch (error) {
      toast.error("Something went wrong");
      console.error(error);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      // Check if question is not empty after trimming
      if (question.trim().length > 0) {
        handleAskQuestion();
      }
    }
  };

  useEffect(() => {
    if (uploadStatus.trim() === "File uploaded successfully") {
      toast.success("File uploaded successfully");
    } else if (uploadStatus.trim() === "File upload failed") {
      toast.info("File upload failed");
    }
  }, [uploadStatus]);

  return (
    <div className="main">
      <ToastContainer />
      <nav>
        <ul>
          <li>
            <img src="/logoreal.svg" alt="Logo" />
          </li>
          <li className="AddPDF">
            {fileSelected ? (
              <div className="file-selected-icon">
                <img
                  src="/check-mark.png"
                  alt="allright"
                  width={24}
                  height={24}
                />
              </div>
            ) : (
              <>
                <input
                  type="file"
                  onChange={handleFileChange}
                  className="input-file"
                  id="fileInput"
                  style={{ display: "none" }}
                  accept=".pdf"
                  disabled={fileSelected}
                />
                <label htmlFor="fileInput" className="upload-button">
                  <div className="circle">
                    <div className="plus"></div>
                  </div>
                  <div>Upload PDF</div>
                </label>
              </>
            )}
          </li>
        </ul>
      </nav>
      <main className="chat-container">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`chat-message ${message.type === "user" ? "user" : "ai"}`}
          >
            {message.text}
          </div>
        ))}
      </main>
      <div className="input-write">
        <input
          placeholder="Enter your question here"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyPress={handleKeyPress} // Handle Enter key press
        />
        <button onClick={handleAskQuestion} disabled={!fileSelected}>
          <img src="/arrow.svg" alt="send" />
        </button>
      </div>
    </div>
  );
}

export default App;
