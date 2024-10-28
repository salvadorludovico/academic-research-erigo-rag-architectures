FROM python:3.12-alpine

WORKDIR /home/python/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/home/python/app:/home/python/app"

COPY requirements.txt .

COPY . .

RUN apk update && apk add --no-cache \
  bash \
  curl \
  openjdk11-jre \
  python3-dev \
  libc6-compat \
  gcc \
  g++ \
  musl-dev \
  geos \
  geos-dev \
  make \
  libc-dev \
  && rm -rf /var/cache/apk/*


ENV GOOGLE_APPLICATION_CREDENTIALS /home/python/app/service-account.json


# Instale o pip e outros requisitos

RUN pip install --upgrade pip


RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app","--host","0.0.0.0"]

# CMD ["tail", "-f", "/dev/null"]