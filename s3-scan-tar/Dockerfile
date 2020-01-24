FROM python:3.8-alpine

RUN apk add --no-cache clamav clamav-dev wget git
RUN wget -nv -O /var/lib/clamav/main.cvd http://database.clamav.net/main.cvd && \
    wget -nv -O /var/lib/clamav/daily.cvd http://database.clamav.net/daily.cvd && \
    wget -nv -O /var/lib/clamav/bytecode.cvd http://database.clamav.net/bytecode.cvd && \
    chown clamav:clamav /var/lib/clamav/*.cvd
RUN mkdir -p /run/clamav && \
    chown clamav:clamav /run/clamav
RUN mkdir -p /opt

COPY start.sh /opt/
COPY s3-scan-tar.py /opt/
COPY requirements.txt /opt/
WORKDIR /opt/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e 'git+https://github.com/arkivverket/mottak#egg=ar_s3_helper&subdirectory=lib/python/ar_s3_helper'


# start up clamd and run the scanner - can be overriden when debugging.
CMD ["/opt/start.sh"]
