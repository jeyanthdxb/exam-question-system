import { useEffect, useState } from "react";
import API from "./api";
import Chat from "./Chat";

function App() {
  const [papers, setPapers] = useState([]);
  const [selectedPaper, setSelectedPaper] = useState("");
  const [questions, setQuestions] = useState([]);
  const [index, setIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState("");

  useEffect(() => {
    loadPapers();
  }, []);

  const loadPapers = async () => {
    try {
      const res = await API.get("/papers");
      setPapers(res.data);
    } catch (error) {
      console.error("Error loading papers:", error);
    }
  };

  const loadQuestions = async (paper) => {
    try {
      const res = await API.get(`/questions/${paper}`);
      setQuestions(res.data);
      setIndex(0);
      setSelectedOption("");
    } catch (error) {
      console.error("Error loading questions:", error);
    }
  };

  const handlePaperChange = (e) => {
    const paper = e.target.value;
    setSelectedPaper(paper);
    loadQuestions(paper);
  };

  const nextQuestion = () => {
    if (index < questions.length - 1) {
      setIndex(index + 1);
      setSelectedOption("");
    }
  };

  const prevQuestion = () => {
    if (index > 0) {
      setIndex(index - 1);
      setSelectedOption("");
    }
  };

  const currentQuestion = questions[index];

  return (
    <div style={{ padding: "30px", maxWidth: "900px", margin: "auto" }}>
      <h2>Exam Question System</h2>

      <select onChange={handlePaperChange} value={selectedPaper}>
        <option value="">Select Paper</option>
        {papers.map((paper) => (
          <option key={paper} value={paper}>
            {paper}
          </option>
        ))}
      </select>

      {currentQuestion && (
        <div style={{ marginTop: "30px" }}>
          <h3>Question {currentQuestion.question_number}</h3>
          <p>{currentQuestion.question_text}</p>

          {/* Images */}
          {currentQuestion.images.map((img, i) => (
            <img
              key={i}
              src={`http://127.0.0.1:8000/extracted_images/${img}`}
              alt="question"
              style={{ maxWidth: "400px", display: "block", marginBottom: "10px" }}
            />
          ))}

          {/* Selectable Options */}
          <div style={{ marginTop: "20px" }}>
            {currentQuestion.options.map((opt, i) => (
              <div key={i} style={{ marginBottom: "8px" }}>
                <label>
                  <input
                    type="radio"
                    name="option"
                    value={opt}
                    checked={selectedOption === opt}
                    onChange={() => setSelectedOption(opt)}
                    style={{ marginRight: "8px" }}
                  />
                  {opt}
                </label>
              </div>
            ))}
          </div>

          <div style={{ marginTop: "20px" }}>
            <button onClick={prevQuestion} disabled={index === 0}>
              Previous
            </button>

            <button
              onClick={nextQuestion}
              disabled={index === questions.length - 1}
              style={{ marginLeft: "10px" }}
            >
              Next
            </button>
          </div>

          <Chat question={currentQuestion.question_text} />
        </div>
      )}
    </div>
  );
}

export default App;