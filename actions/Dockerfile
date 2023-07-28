FROM python:3.8.6

WORKDIR /app

COPY . /app


RUN pip install --no-cache-dir -r requirements.txt
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs

EXPOSE 5055


CMD ["rasa", "run", "actions"]