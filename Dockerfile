# FROM python:3

# ENV PYTHONUNBUFFERED 1
# RUN mkdir /libo_api
# WORKDIR /libo_api
# COPY . /libo_api/
# RUN pip install -r requirements.txt

# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the current directory contents into the container at /code/
COPY . /code/

# Expose port 8000 to the outside world
EXPOSE 8000

# Run Django application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
