# FROM python:3.11.2-slim-buster
# FROM python:3.8.13-slim-buster
FROM python:3.9.18-slim-bookworm

ENV PYTHONUNBUFFERED=1

EXPOSE 8501

WORKDIR /app

COPY requirements.txt ./requirements.txt
COPY Makefile ./Makefile
COPY . .

RUN apt-get update && apt-get install -y make git libpq-dev gcc g++ nano
# RUN apt-get update && apt-get install -y make git libpq-dev gcc g++ nano ffmpeg libsm6 libxext6  -y
# RUN apk update && apk add --no-cache make git libpq-dev gcc g++ nano
RUN pip install --upgrade pip
RUN make install

CMD ["make", "run"]