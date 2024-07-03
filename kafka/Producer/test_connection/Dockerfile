FROM python:3.9

WORKDIR /app

# Update package list and install wget
RUN apt-get update && \
    apt-get install -y wget

# Copy requirements.txt and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy get-data.py
COPY get-data.py get-data.py

# Set the entry point
ENTRYPOINT [ "python", "get-data.py" ]