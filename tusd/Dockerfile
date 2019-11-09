# Please note; chained build-
FROM alpine:3.9

COPY  artifacts/tusd /usr/local/bin/
COPY  artifacts/kubectl /usr/local/bin/
COPY  artifacts/argo /usr/local/bin/
 



# CA for networking
# curl for installing kubectl
# bash for convenience
RUN apk add --no-cache ca-certificates jq gcc curl bash \
    && addgroup -g 1000 tusd \
    && adduser -u 1000 -G tusd -s /bin/sh -D tusd \
    && mkdir -p /srv/tusd-hooks \
    && mkdir -p /srv/tusd-data \
    && chown tusd:tusd /srv/tusd-data

COPY tusd-hooks  /srv/

# Set the environment variable to grants access to GCS
# This should be referenced in the deployment.yaml
ENV GCS_SERVICE_ACCOUNT_FILE=/etc/gcs/gcs.json

# Set up k8s


WORKDIR /srv/tusd-data
EXPOSE 1080
CMD ["tusd","--hooks-dir","/srv/tusd-hooks"]

USER tusd