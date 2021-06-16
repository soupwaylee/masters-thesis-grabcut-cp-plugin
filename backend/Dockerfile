FROM alpine

RUN apk add python3 python3-dev py3-pip py3-wheel alpine-sdk postgresql-dev

RUN pip3 install --no-cache-dir gunicorn

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

#COPY . .

WORKDIR /usr/src/app/src

EXPOSE 5000
ENV SCRIPT_NAME="/grabcut" PORT="5000" FLASK_APP="app:app"

ENTRYPOINT flask db upgrade && flask db migrate && flask db upgrade && gunicorn --reload --reload-engine=poll app:app