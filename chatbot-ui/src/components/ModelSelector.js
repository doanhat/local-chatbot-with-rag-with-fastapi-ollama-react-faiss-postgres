import React from 'react';
import { FormControl, InputLabel, Select, MenuItem, Typography } from '@mui/material';

function ModelSelector({ models, selectedModel, onSelectModel }) {
  const hasError = models.length === 1 && models[0].error;

  return (
    <FormControl fullWidth variant="outlined" style={{ marginBottom: 20 }}>
      <InputLabel>Select Model</InputLabel>
      <Select
        value={selectedModel}
        onChange={(e) => onSelectModel(e.target.value)}
        label="Select Model"
        disabled={hasError}
      >
        {hasError ? (
          <MenuItem value="">
            <Typography color="error">{models[0].name}</Typography>
          </MenuItem>
        ) : (
          models.map((model) => (
            <MenuItem key={model.name} value={model.name}>
              {model.name}
            </MenuItem>
          ))
        )}
      </Select>
      {hasError && (
        <Typography color="error" variant="caption">
          {models[0].error}
        </Typography>
      )}
    </FormControl>
  );
}

export default ModelSelector;
