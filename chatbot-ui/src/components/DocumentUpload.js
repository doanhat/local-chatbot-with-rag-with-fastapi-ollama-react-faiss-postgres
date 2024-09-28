import React, { useState } from 'react';
import { Button, Typography } from '@mui/material';
import { uploadDocument } from '../services/api';

function DocumentUpload() {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    try {
      await uploadDocument(file);
      alert('Document uploaded successfully!');
      setFile(null);
    } catch (error) {
      console.error('Error uploading document:', error);
      alert('Error uploading document. Please try again.');
    }
  };

  return (
    <div style={{ marginBottom: 20 }}>
      <Typography variant="h6" gutterBottom>
        Upload Document
      </Typography>
      <input
        accept=".pdf,.docx,.txt"
        style={{ display: 'none' }}
        id="raised-button-file"
        type="file"
        onChange={handleFileChange}
      />
      <label htmlFor="raised-button-file">
        <Button variant="contained" component="span">
          Choose File
        </Button>
      </label>
      {file && <Typography>{file.name}</Typography>}
      <Button
        variant="contained"
        color="primary"
        onClick={handleUpload}
        disabled={!file}
        style={{ marginLeft: 10 }}
      >
        Upload
      </Button>
    </div>
  );
}

export default DocumentUpload;
