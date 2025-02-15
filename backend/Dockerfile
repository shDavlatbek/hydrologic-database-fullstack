# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose port used by FastAPI
EXPOSE 8198

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8198", "--workers", "4"]

