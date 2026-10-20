# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency list and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source code, data, and trained model artifacts
COPY src/ ./src/
COPY data/ ./data/
COPY models/ ./models/

# Expose port for FastAPI
EXPOSE 8000

# Run Uvicorn server when container starts
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]