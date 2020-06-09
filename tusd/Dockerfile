FROM argoproj/argocli:latest AS argocli
FROM tusio/tusd:v1.0.1

USER root
RUN apk add --no-cache \
    bash \
    curl \
    musl-dev \
    postgresql-client \
    postgresql-dev \
    python3 \
    python3-dev \
    libffi-dev \
    make cmake \
    g++ gcc
RUN pip3 install --upgrade pip
RUN pip3 install \
    psycopg2 \
    python-dotenv \
    azure-servicebus
# Note how use the same script for both hooks.
COPY tusd-hooks/pre-create  /srv/tusd-hooks/pre-create
COPY tusd-hooks/pre-create  /srv/tusd-hooks/post-finish

RUN wget https://github.com/argoproj/argo/releases/download/v2.8.0/argo-linux-amd64 && \
    chmod +x argo-linux-amd64 && \
    mv argo-linux-amd64 /usr/local/bin/argo

WORKDIR /srv/tusd-data
EXPOSE 1080
COPY start.sh /srv/
CMD ["/srv/start.sh"]

