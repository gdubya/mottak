# Please note; chained build-

FROM golang:1.12-alpine AS builder

# Copy in the git repo from the build context
COPY tusd /go/src/github.com/tus/tusd/

# Create app directory
WORKDIR /go/src/github.com/tus/tusd

RUN apk add --no-cache \
        git gcc libc-dev \
    && go get -d -v ./... \
    && version="$(git tag -l --points-at HEAD)" \
    && commit=$(git log --format="%H" -n 1) \
    && GOOS=linux GOARCH=amd64 go build \
        -ldflags="-X github.com/tus/tusd/cmd/tusd/cli.VersionName=${version} -X github.com/tus/tusd/cmd/tusd/cli.GitCommit=${commit} -X 'github.com/tus/tusd/cmd/tusd/cli.BuildDate=$(date --utc)'" \
        -o "/go/bin/tusd" ./cmd/tusd/main.go \
    && rm -r /go/src/* \
    && apk del git

# start a new stage that copies in the binary built in the previous stage
FROM alpine:3.9

COPY --from=builder /go/bin/tusd /usr/local/bin/tusd

# CA for networking
# curl for installing kubectl
# bash for convenience
RUN apk add --no-cache ca-certificates jq gcc curl bash \
    && addgroup -g 1000 tusd \
    && adduser -u 1000 -G tusd -s /bin/sh -D tusd \
    && mkdir -p /srv/tusd-hooks \
    && mkdir -p /srv/tusd-data \
    && chown tusd:tusd /srv/tusd-data

# Set the environment variable to grants access to GCS
# This should be referenced in the deployment.yaml
ENV GCS_SERVICE_ACCOUNT_FILE=/etc/gcs/gcs.json

# Set up k8s
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin


WORKDIR /srv/tusd-data
EXPOSE 1080
CMD ["tusd","--hooks-dir","/srv/tusd-hooks"]

USER tusd