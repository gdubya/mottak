FROM python:3.7-alpine

RUN mkdir -p /opt
COPY s3-checksum256.py /opt
COPY requirements.txt /opt
WORKDIR /opt
RUN pip install --no-cache-dir -r requirements.txt


# start up clamd and run the scanner
ENTRYPOINT /opt/s3-checksum256.py
# When debugging set the entrypoint to the shell.
# ENTRYPOINT /bin/sh 
