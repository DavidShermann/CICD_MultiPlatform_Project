FROM python:3.10-slim-buster

WORKDIR /project

COPY . .

RUN python3 -m pip install --upgrade pip -y 

RUN python3 -m pip install -r requirements.txt -y

EXPOSE 5000

CMD gunicorn --workers 1 --bind 0.0.0.0:5000 app:app 

