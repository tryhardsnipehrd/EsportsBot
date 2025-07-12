FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY .env ./bot/
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD [ "python", "./bot/main.py" ]