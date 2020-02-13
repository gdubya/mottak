FROM python:3.8-alpine

RUN apk add --no-cache clamav clamav-dev wget git py3-cryptography py3-apache-libcloud py3-requests
RUN wget -nv -O /var/lib/clamav/main.cvd http://database.clamav.net/main.cvd && \
    wget -nv -O /var/lib/clamav/daily.cvd http://database.clamav.net/daily.cvd && \
    wget -nv -O /var/lib/clamav/bytecode.cvd http://database.clamav.net/bytecode.cvd && \
    chown clamav:clamav /var/lib/clamav/*.cvd
RUN mkdir -p /run/clamav && \
    chown clamav:clamav /run/clamav
RUN mkdir -p /opt

COPY start.sh /opt/
COPY s3-scan-tar.py /opt/
WORKDIR /opt/

RUN pip install -e 'git+https://github.com/arkivverket/mottak#egg=av_objectstore&subdirectory=lib/python/av_objectstore'
RUN pip install pyClamd python-dotenv
# We are currently running as root in order to start clamav....
# RUN addgroup -S molgroup && adduser -S mol -G molgroup
# USER mol
ENV PYTHONPATH "$PYTHONPATH:/usr/lib/python3.8/site-packages"
COPY gcs.json /opt
# start up clamd and run the scanner - can be overriden when debugging.
CMD ["/opt/start.sh"]
