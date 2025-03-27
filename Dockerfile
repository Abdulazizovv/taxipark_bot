# Use the official Python image
FROM python:3.12.3-alpine

# Set the working directory inside the container
WORKDIR /usr/src/app

# Prevent Python from writing .pyc files and buffer output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /usr/src/app/requirements.txt

# Copy the entire project into the container
COPY ./config /usr/src/app/

