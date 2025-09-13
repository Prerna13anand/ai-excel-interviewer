import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    // Create history from messages, excluding the last user message
    const history = newMessages.slice(0, -1).map(msg => ({
      role: msg.role === 'ai' ? 'model' : 'user',
      content: msg.content
    }));

    try {
      const response = await axios.post('https://ai-excel-interviewer.onrender.com/chat', {
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

  return (
    <div className="App">
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <p>{msg.content}</p>
          </div>
        ))}
        {isLoading && <div className="message ai"><p>Thinking...</p></div>}
      </div>
      <form onSubmit={handleSubmit} className="chat-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about Excel..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default App;
