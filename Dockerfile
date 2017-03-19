FROM python:3.6-alpine

WORKDIR /app

RUN apk update --no-cache && \
    apk upgrade --no-cache

RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "-u", "gameserver.py"]
