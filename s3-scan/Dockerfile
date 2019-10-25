FROM python:3.7-alpine

RUN apk add --no-cache clamav wget
RUN wget -O /var/lib/clamav/main.cvd http://database.clamav.net/main.cvd && \
    wget -O /var/lib/clamav/daily.cvd http://database.clamav.net/daily.cvd && \
    wget -O /var/lib/clamav/bytecode.cvd http://database.clamav.net/bytecode.cvd && \
    chown clamav:clamav /var/lib/clamav/*.cvd
RUN mkdir -p /run/clamav
RUN mkdir -p /opt

COPY s3-avscan.py /opt/s3-avscan.py
COPY requirements.txt /opt
WORKDIR /opt
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT /bin/sh
