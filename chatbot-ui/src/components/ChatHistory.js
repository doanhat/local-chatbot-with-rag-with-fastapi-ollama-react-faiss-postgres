import React, { useState, useEffect } from 'react';
import { List, ListItem, ListItemText, Typography, Paper } from '@mui/material';
import { fetchChatHistory } from '../services/api';

function ChatHistory() {
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const getHistory = async () => {
      try {
        setIsLoading(true);
        const chatHistory = await fetchChatHistory();
        setHistory(chatHistory.chat_history || []);
      } catch (error) {
        console.error('Error fetching chat history:', error);
        setHistory([]);
      } finally {
        setIsLoading(false);
      }
    };
    getHistory();
  }, []);

  if (isLoading) {
    return <Typography>Loading chat history...</Typography>;
  }

  return (
    <div>
      <Typography variant="h6" gutterBottom>
        Chat History
      </Typography>
      <Paper style={{ maxHeight: 300, overflow: 'auto' }}>
        <List>
          {Array.isArray(history) && history.map((item, index) => (
            <ListItem key={index} alignItems="flex-start">
              <ListItemText
                primary={`User: ${item.user_input}`}
                secondary={`Bot: ${item.bot_response}`}
              />
            </ListItem>
          ))}
        </List>
      </Paper>
    </div>
  );
}

export default ChatHistory;
