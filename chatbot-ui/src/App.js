import React, { useState, useEffect } from 'react';
import { Container, Paper, Typography } from '@mui/material';
import Chat from './components/Chat';
import ModelSelector from './components/ModelSelector';
import DocumentUpload from './components/DocumentUpload';
import ChatHistory from './components/ChatHistory';
import { fetchModels } from './services/api';

function App() {
  const [selectedModel, setSelectedModel] = useState('');
  const [models, setModels] = useState([]);

  useEffect(() => {
    const getModels = async () => {
      try {
        const availableModels = await fetchModels();
        console.log("Fetched models:", availableModels);
        setModels(availableModels);
        if (availableModels.length > 0) {
          setSelectedModel(availableModels[0].name);
        } else {
          console.warn("No models available");
        }
      } catch (error) {
        console.error("Error fetching models:", error);
      }
    };
    getModels();
  }, []);

  return (
    <Container maxWidth="md">
      <Paper elevation={3} style={{ padding: '20px', marginTop: '20px' }}>
        <Typography variant="h4" gutterBottom>
          AI Chatbot
        </Typography>
        <ModelSelector
          models={models}
          selectedModel={selectedModel}
          onSelectModel={setSelectedModel}
        />
        <DocumentUpload />
        <Chat selectedModel={selectedModel} />
        <ChatHistory />
      </Paper>
    </Container>
  );
}

export default App;
