import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [report, setReport] = useState('');
  const [isInterviewOver, setIsInterviewOver] = useState(false);

  // --- IMPORTANT: Use your deployed Render URL here ---
  const API_BASE_URL = 'https://ai-excel-interviewer.onrender.com';

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isInterviewOver) return;

    const userMessage = { role: 'user', content: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    const history = newMessages.slice(0, -1);

    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        message: input,
        history: history,
      });
      const aiMessage = { role: 'ai', content: response.data.response };
      setMessages([...newMessages, aiMessage]);
    } catch (error) {
      console.error("Error fetching response:", error);
      const errorMessage = { role: 'ai', content: 'Sorry, I ran into an error. Please try again.' };
      setMessages([...newMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGetReport = async () => {
    setIsLoading(true);
    setIsInterviewOver(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/report`, {
        history: messages,
      });
      setReport(response.data.report);
    } catch (error) {
      console.error("Error fetching report:", error);
      setReport('Sorry, there was an error generating your report.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <p>{msg.content}</p>
          </div>
        ))}
        {isLoading && <div className="message ai"><p>Thinking...</p></div>}
        {isInterviewOver && report && (
          <div className="report-container">
            <h2>Interview Performance Report</h2>
            <pre className="report-text">{report}</pre>
          </div>
        )}
      </div>
      {!isInterviewOver ? (
        <form onSubmit={handleSubmit} className="chat-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about Excel..."
          />
          <button type="submit">Send</button>
        </form>
      ) : null}
      <div className="report-button-container">
          {!isInterviewOver && messages.length > 0 && (
            <button onClick={handleGetReport} className="report-button">
              End Interview & Get Report
            </button>
          )}
      </div>
    </div>
  );
}

export default App;