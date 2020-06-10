
FROM debian:buster-slim

RUN apt-get update \
    && apt-get install -y wget ca-certificates jq gcc postgresql-client python3 python3-dev python3-pip python3-psycopg2 \
    && apt-get clean

RUN wget -q https://github.com/tus/tusd/releases/download/v1.3.0/tusd_snapshot_amd64.deb && \
    dpkg -i tusd_snapshot_amd64.deb && \
    apt install -yf

RUN mkdir -p /srv/tusd-hooks \
    && mkdir -p /srv/tusd-data \
    && useradd --system --user-group tusd \
    && chown tusd:tusd /srv/tusd-data

# RUN pip3 install --upgrade pip
RUN pip3 install azure-servicebus
WORKDIR /srv/tusd-data
COPY tusd-hooks/pre-create  /srv/tusd-hooks/pre-create
COPY tusd-hooks/pre-create  /srv/tusd-hooks/post-finish

RUN wget -q https://github.com/argoproj/argo/releases/download/v2.8.0/argo-linux-amd64 && \
    chmod +x argo-linux-amd64 && \
    mv argo-linux-amd64 /usr/local/bin/argo

EXPOSE 1080
USER tusd

CMD ["/srv/start.sh"]
