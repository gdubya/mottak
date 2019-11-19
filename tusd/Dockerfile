FROM alpine:3.9

ADD artifacts/artifacts.tar.gz /usr/local/bin

# CA for networking
# curl for installing kubectl
# bash for convenience
RUN apk add --no-cache ca-certificates jq gcc curl bash \
    && addgroup -g 1000 tusd \
    && adduser -u 1000 -G tusd -s /bin/sh -D tusd \
    && mkdir -p /srv/tusd-hooks \
    && mkdir -p /srv/tusd-data \
    && chown tusd:tusd /srv/tusd-data

RUN apk add --no-cache python3 postgresql-dev gcc python3-dev musl-dev \
    && apk add  --no-cache postgresql-client \
    && pip3 install psycopg2 \
    && pip3 install python-dotenv

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
