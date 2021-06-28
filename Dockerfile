# syntax=docker/dockerfile:1
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
RUN apt-get install -y python3.9-venv

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python3.9 -m pip install --upgrade pip
RUN python3.9 -m venv /venv
ENV PATH=/venv/bin:$PATH

# Need to install Geos and Proj for Cartopy
RUN apt-get install -y libproj-dev proj-data proj-bin  
RUN apt-get install -y libgeos-dev

# Need to install GDAL specific version
RUN apt-get install -y gdal-bin=3.2.1+dfsg-1~focal0
RUN apt-get install -y libgdal-dev=3.2.1+dfsg-1~focal0

# Some packages needed for both GDAL and Cartopy
RUN python -m pip install wheel
RUN python -m pip install cython
RUN python -m pip install cartopy

# Export env variable for GDAL and install the specific version compatible
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
RUN python -m pip install GDAL==3.2.1

# Get and install packages needed for api-mmo 
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt


ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000


# Copy in the application code from your work station at the current directory
# over to the working directory.
COPY . .

RUN chmod 755 app-entrypoint.sh

ENTRYPOINT ["/app/app-entrypoint.sh", "db"]
