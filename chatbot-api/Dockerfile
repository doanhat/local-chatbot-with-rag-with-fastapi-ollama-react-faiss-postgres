# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install
COPY dist/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Command to run your application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
