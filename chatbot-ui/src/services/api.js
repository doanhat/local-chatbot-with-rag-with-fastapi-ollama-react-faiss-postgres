import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

export const fetchModels = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/models`);
    return Array.isArray(response.data.models) ? response.data.models : [];
  } catch (error) {
    console.error('Error fetching models:', error);
    return [];
  }
};

export const sendMessage = async (model, message) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/chat`, { model, message });
    return response.data;
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};

export const uploadDocument = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    const headers = {
      'Content-Type': 'multipart/form-data'
    };
    const response = await axios.post(`${API_BASE_URL}/documents/upload`, formData, {
      headers: headers,
      timeout: 30000 // 30 seconds timeout
    });
    console.log('Upload response:', response);
    return response.data;
  } catch (error) {
    console.error('Error uploading document:', error);
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('Error response:', error.response.data);
      console.error('Error status:', error.response.status);
      console.error('Error headers:', error.response.headers);
    } else if (error.request) {
      // The request was made but no response was received
      console.error('Error request:', error.request);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('Error message:', error.message);
    }
    throw error;
  }
};

export const fetchChatHistory = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/chat/history`);
    return response.data; // Assuming this returns { chat_history: [...] }
  } catch (error) {
    console.error('Error fetching chat history:', error);
    return { chat_history: [] }; // Return an object with an empty array on error
  }
};

