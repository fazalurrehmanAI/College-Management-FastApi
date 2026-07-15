FROM python:3.12-slim

# Prevent python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Show python output immediately
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI
CMD ["sh", "-c", "uvicorn college_api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]