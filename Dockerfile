# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port and run
EXPOSE 8501
CMD ["streamlit", "run", "main.py"]
