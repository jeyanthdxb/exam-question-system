import { useState } from "react";
import API from "./api";

function Chat({ question }) {
  const [input, setInput] = useState("");
  const [reply, setReply] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    try {
      setLoading(true);

      const res = await API.post("/chat", {
        question: question,
        message: input,
      });

      setReply(res.data.reply);
    } catch (error) {
      setReply("Error contacting tutor.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: "20px", padding: "10px", border: "1px solid #ccc" }}>
      <h4>Ask the Tutor</h4>

      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask your doubt..."
        style={{ width: "70%", marginRight: "10px" }}
      />

      <button onClick={sendMessage}>Ask</button>

      {loading && <p>Thinking...</p>}

      {reply && (
        <div style={{ marginTop: "10px", background: "#f4f4f4", padding: "10px" }}>
          <strong>Tutor:</strong>
          <p>{reply}</p>
        </div>
      )}
    </div>
  );
}

export default Chat;