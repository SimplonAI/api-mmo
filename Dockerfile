# syntax=docker/dockerfile:1
<<<<<<< HEAD
FROM ubuntu:20.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/*
RUN add-apt-repository ppa:ubuntugis/ppa -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get update
RUN apt-get install -y python3.9
RUN apt-get install -y build-essential libssl-dev libffi-dev python3.9-dev
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-venv

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python3.9 -m pip install --upgrade pip


# Need to install Geos and Proj for Cartopy
RUN apt-get install -y libproj-dev proj-data proj-bin  
RUN apt-get install -y libgeos-dev

# Need to install GDAL specific version
RUN apt-get install -y gdal-bin=3.2.1+dfsg-1~focal0
RUN apt-get install -y libgdal-dev=3.2.1+dfsg-1~focal0

# Some packages needed for both GDAL and Cartopy
RUN python3.9 -m pip install wheel
RUN python3.9 -m pip install cython
RUN python3.9 -m pip install cartopy

# Export env variable for GDAL and install the specific version compatible
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
RUN python3.9 -m pip install GDAL==3.2.1

# Get and install packages needed for api-mmo 
COPY requirements.txt requirements.txt
RUN python3.9 -m pip install -r requirements.txt


ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000


# Copy in the application code from your work station at the current directory
# over to the working directory.
=======
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

>>>>>>> e13e2267f607ff2a7b6b3afbe4833bb4ea435def
COPY . .

RUN chmod 755 app-entrypoint.sh

ENTRYPOINT ["/app/app-entrypoint.sh", "db"]
