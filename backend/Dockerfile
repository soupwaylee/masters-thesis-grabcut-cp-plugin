FROM python:buster

RUN pip3 install --no-cache-dir gunicorn

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt update

RUN apt install libgl1-mesa-glx -y

RUN pip3 install --no-cache-dir -r requirements.txt

#COPY . .

WORKDIR /usr/src/app/src

EXPOSE 5000
ENV SCRIPT_NAME="/grabcut" PORT="5000" FLASK_APP="app:app"

ENTRYPOINT flask db upgrade && flask db migrate && flask db upgrade && gunicorn --reload --reload-engine=poll app:app