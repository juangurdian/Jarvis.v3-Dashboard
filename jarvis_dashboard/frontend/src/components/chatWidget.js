// src/components/ChatWidget.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/ChatWidget.css';

function ChatWidget() {
  const [inputMessage, setInputMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  // Function to send a message to the backend
  const sendMessage = async () => {
    if (!inputMessage.trim()) return;
    try {
      // Send the message to the backend
      const response = await axios.post('http://127.0.0.1:5000/api/chat', {
        message: inputMessage,
      });
      // Instead of appending manually, we can re-fetch the history after sending.
      // However, for immediate update we can also update state as follows:
      setChatHistory(prev => [
        ...prev,
        { role: 'user', message: inputMessage },
        { role: 'assistant', message: response.data.response },
      ]);
      setInputMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  // Fetch chat history on mount and poll every 3 seconds for updates.
  useEffect(() => {
    const fetchChatHistory = async () => {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/chat');
        // res.data.chat_history is an array of objects with keys "role" and "content"
        // Map them to keys "role" and "message" for consistency.
        const history = res.data.chat_history.map(chat => ({
          role: chat.role,
          message: chat.content,
        }));
        setChatHistory(history);
      } catch (error) {
        console.error('Error fetching chat history:', error);
      }
    };

    // Fetch initially
    fetchChatHistory();

    // Set up polling every 3 seconds
    const intervalId = setInterval(() => {
      fetchChatHistory();
    }, 3000);

    // Clean up on unmount
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="chat-widget">
      <div className="chat-history">
        {chatHistory.map((chat, index) => (
          <div key={index} className={chat.role}>
            <strong>{chat.role === 'assistant' ? 'Jarvis' : 'You'}:</strong> {chat.message}
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default ChatWidget;
