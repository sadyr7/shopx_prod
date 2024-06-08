# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install  gunicorn --no-cache-dir && pip install --no-cache-dir -r requirements.txt



# Обновление пакетов и установка Redis
RUN apt-get update && apt-get install -y redis-server



COPY . /app/



# Run the entrypoint script when the container starts
CMD ["bash", "entrypoint.sh"]

# sudo apt install nginx