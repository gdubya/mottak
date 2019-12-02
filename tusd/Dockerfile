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
    python3-dev

RUN pip3 install \
    psycopg2 \
    python-dotenv

# Note how use the same script for both hooks.
COPY tusd-hooks/pre-create  /srv/tusd-hooks/pre-create
COPY tusd-hooks/pre-create  /srv/tusd-hooks/post-finish
COPY argo-mottak-DAG.yaml /srv/
COPY --from=argocli /bin/argo /usr/local/bin/argo

# Set the environment variable to grants access to GCS
# This should be referenced in the deployment.yaml
ENV GCS_SERVICE_ACCOUNT_FILE=/etc/gcs/gcs.json

WORKDIR /srv/tusd-data
EXPOSE 1080
COPY start.sh /srv/
ENTRYPOINT ["/srv/start.sh"]

USER tusd
