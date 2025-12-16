# Use a base image with Python
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt  # Install dependencies

# Copy the rest of your application code
COPY . .

# Expose the port that Chainlit uses (default is 8501)
EXPOSE 8501

# Command to run the Chainlit application
CMD ["chainlit", "run", "model.py", "-w", "--port", "8501"]