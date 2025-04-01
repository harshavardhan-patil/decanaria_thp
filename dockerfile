FROM python:3.9

WORKDIR /decanaria_thp

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Set environment variables
ENV PYTHONPATH=/decanaria_thp

# Override post start command in docker-compose
CMD ["python", "-c", "import time; time.sleep(3600)"]