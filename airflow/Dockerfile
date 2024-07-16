FROM apache/airflow:latest

# Copy the requirements.txt file into the image
COPY requirements.txt /requirements.txt

# Install pip and requirements globally in the virtual environment
RUN pip install --upgrade pip \
    && pip install -r /requirements.txt
