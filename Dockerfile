# syntax=docker/dockerfile:1
# specify the image you want to use build docker image
FROM python:3.9.5-slim-buster

WORKDIR /app

ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy in the application code from your work station at the current directory
# over to the working directory.

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .

RUN chmod 755 app-entrypoint.sh

ENTRYPOINT ["/app/app-entrypoint.sh", "db"]
