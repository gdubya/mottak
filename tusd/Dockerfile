FROM alpine:3.10

ADD artifacts/artifacts.tar.gz /usr/local/bin

# CA for networking
# curl for installing kubectl
# bash for convenience
RUN apk add --no-cache \
    bash \
    ca-certificates \
    curl \
    gcc \
    jq \
    musl-dev \
    postgresql-client \
    postgresql-dev \
    python3 \
    python3-dev

RUN addgroup -g 1000 tusd \
    && adduser -u 1000 -G tusd -s /bin/sh -D tusd \
    && mkdir -p /srv/tusd-hooks \
    && mkdir -p /srv/tusd-data \
    && chown tusd:tusd /srv/tusd-data

RUN pip3 install \
    psycopg2 \
    python-dotenv

# Note how use the same script for both hooks.
COPY tusd-hooks/pre-create  /srv/tusd-hooks/pre-create
COPY tusd-hooks/pre-create  /srv/tusd-hooks/post-finish
COPY argo-mottak-DAG.yaml /srv/

# Set the environment variable to grants access to GCS
# This should be referenced in the deployment.yaml
ENV GCS_SERVICE_ACCOUNT_FILE=/etc/gcs/gcs.json

# Set up k8s


WORKDIR /srv/tusd-data
EXPOSE 1080
CMD ["tusd","-behind-proxy","-hooks-dir","/srv/tusd-hooks"]

USER tusd
