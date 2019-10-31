FROM python:3.7-alpine

RUN mkdir -p /opt
COPY s3-checksum256.py /opt
COPY requirements.txt /opt
WORKDIR /opt
RUN pip install --no-cache-dir -r requirements.txt


# run the scanner - can be overriden when debugging.
CMD ["/opt/s3-checksum256.py"]
