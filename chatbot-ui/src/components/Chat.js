import React, { useState } from 'react';
import { TextField, Button, List, ListItem, ListItemText, Paper } from '@mui/material';
import { sendMessage } from '../services/api';

function Chat({ selectedModel }) {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const handleSendMessage = async () => {
    if (message.trim() === '') return;

    const userMessage = { text: message, sender: 'user' };
    setChatHistory([...chatHistory, userMessage]);
    setMessage('');

    try {
      const response = await sendMessage(selectedModel, message);
      const botMessage = { text: response.message, sender: 'bot' };
      setChatHistory(prevHistory => [...prevHistory, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      // Add user-friendly error handling here
      const errorMessage = { text: "Sorry, an error occurred. Please try again.", sender: 'bot' };
      setChatHistory(prevHistory => [...prevHistory, errorMessage]);
    }
  };

  return (
    <div>
      <Paper style={{ maxHeight: 300, overflow: 'auto', marginBottom: 20 }}>
        <List>
          {chatHistory.map((msg, index) => (
            <ListItem key={index} alignItems="flex-start">
              <ListItemText
                primary={msg.sender === 'user' ? 'You' : 'Bot'}
                secondary={msg.text}
              />
            </ListItem>
          ))}
        </List>
      </Paper>
      <TextField
        fullWidth
        variant="outlined"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message here"
      />
      <Button
        variant="contained"
        color="primary"
        onClick={handleSendMessage}
        style={{ marginTop: 10 }}
      >
        Send
      </Button>
    </div>
  );
}

export default Chat;
