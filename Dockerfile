FROM python:3.12.4

WORKDIR /home/python/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/home/python/app:/home/python/app"

COPY requirements.txt .

COPY . .

# RUN apk update && apk add --no-cache \
#   bash \
#   curl \
#   openjdk11-jre \
#   python3-dev \
#   libc6-compat \
#   gcc \
#   g++ \
#   musl-dev \
#   geos \
#   geos-dev \
#   make \
#   libc-dev \
#   && rm -rf /var/cache/apk/*


# Baixe e instale o SDK do Google Cloud
# Downloading gcloud package
# RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

# RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
#   source $HOME/.cargo/env && \
#   rustc --version

# Installing the package
# RUN mkdir -p /usr/local/gcloud \
#   && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
#   && /usr/local/gcloud/google-cloud-sdk/install.sh

# Adding the package path to local
# ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin
ENV GOOGLE_APPLICATION_CREDENTIALS /home/python/app/service-account.json

# RUN gcloud auth activate-service-account --key-file=/home/python/app/service-account.json

# RUN gcloud config set project energygpt-421317
# RUN gcloud config set compute/region us-east1 

# Instale o pip e outros requisitos

RUN pip install --upgrade pip

# RUN pip install -r requirements.txt
RUN pip install uvicorn

EXPOSE 8000

# CMD ["uvicorn", "main:app","--host","0.0.0.0"]

CMD ["tail", "-f", "/dev/null"]