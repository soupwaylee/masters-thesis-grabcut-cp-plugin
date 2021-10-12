FROM python:3.9-slim-buster

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y build-essential libgl1-mesa-glx python3-dev libpq-dev && \
    apt-get clean -y && \
    apt-get autoclean -y

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

#COPY . .

WORKDIR /usr/src/app/src

EXPOSE 5000
ENV SCRIPT_NAME="/grabcut" PORT="5000" FLASK_APP="app:app"

ENTRYPOINT flask db upgrade && flask db migrate && flask db upgrade && gunicorn --reload --reload-engine=poll --timeout $CP_DEV_GUNICORN_TIMEOUT app:app