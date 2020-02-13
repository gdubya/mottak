FROM python:3.8-alpine
RUN apk add --no-cache git py3-cryptography py3-apache-libcloud py3-requests

RUN mkdir -p /opt
COPY s3-checksum256.py /opt
WORKDIR /opt
# We don't need requirements.txt - we get native packages from debian.
# Install the helper module:
RUN pip install -e 'git+https://github.com/arkivverket/mottak#egg=av_objectstore&subdirectory=lib/python/av_objectstore'
RUN pip install python-dotenv
RUN addgroup -S molgroup && adduser -S mol -G molgroup
USER mol
# alpine seems to be a bit stupid wrt PYTHONPATH handling.
ENV PYTHONPATH "$PYTHONPATH:/usr/lib/python3.8/site-packages"
# COPY gcs.json /opt
# run the scanner - can be overriden when debugging.
CMD ["/opt/s3-checksum256.py"]
