# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /bookRec_docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Set the environment variable for Flask
ENV FLASK_APP=server.py  


CMD ["flask", "run", "--host=0.0.0.0", "--port=6000"]
