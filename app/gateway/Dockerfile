FROM python:3.10-slim-buster

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gunicorn && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

USER nobody

ENTRYPOINT [ "./entrypoint.sh" ]
