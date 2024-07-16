
FROM apache/airflow:latest

# Switch to root to install system dependencies
USER root

# Install system dependencies (if any)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt /requirements.txt

# Install python dependencies
RUN pip install --upgrade pip \
    && pip install -r /requirements.txt

# Switch to airflow user
USER airflow
