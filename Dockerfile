FROM python:3.8.6
WORKDIR /app

COPY . /app


RUN pip install --no-cache-dir -r requirements.txt

RUN rasa train

USER 1001


CMD ["rasa", "run", "--enable-api", "--port", "8080"]