FROM python:slim

ENV PYTHONDONTWRITEBYTECODE = 1 \
    PYTHONUNBUFFERED = 1

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get-clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY . .

RUN pip install --no-cache-dir -e .

RUN python pipeline/training_pipeline.py

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "application.py"]

