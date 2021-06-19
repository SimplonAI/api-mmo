# specify the image you want to use build docker image
FROM python:3.9.5-slim-buster
#apt is the ubuntu command line tool for advanced packaging tool(APT) for sw upgrade '''

#RUN apt update && \ apt install -y netcat-openbsd
EXPOSE 5000
#RUN apt-get install -y python-pip python-dev


# set the env variable to tell where the app will be installed inside the docker

ENV INSTALL_PATH /API-IMO
RUN mkdir -p $INSTALL_PATH

#this sets the context of where commands will be ran in and is documented

WORKDIR $INSTALL_PATH

# Copy in the application code from your work station at the current directory
# over to the working directory.

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY . .


#RUN chmod +x /API-IMO/API-IMO-entrypoint.sh
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
RUN chmod +x /API-IMO/API-IMO-entrypoint.sh
CMD ["/bin/bash", "/API-IMO/API-IMO-entrypoint.sh"]
