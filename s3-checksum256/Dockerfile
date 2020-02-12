FROM python:3.8-slim
#RUN apk add --no-cache git py3-cryptography
RUN apt-get update && apt-get install -y --no-install-recommends git python3-cryptography python3-dotenv
RUN mkdir -p /opt
COPY s3-checksum256.py /opt
WORKDIR /opt
# We don't need requirements.txt - we get native packages from debian.
COPY requirements.txt /opt
RUN pip install --no-cache-dir -r requirements.txt
# Install the helper module:
RUN pip install -e 'git+https://github.com/arkivverket/mottak#egg=av_objectstore&subdirectory=lib/python/av_objectstore'


# run the scanner - can be overriden when debugging.
CMD ["/opt/s3-checksum256.py"]
