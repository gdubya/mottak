FROM python:3.7-alpine
RUN apk add --no-cache git
RUN mkdir -p /opt
COPY s3-rename.py /opt
COPY requirements.txt /opt
WORKDIR /opt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e 'git+https://github.com/arkivverket/mottak#egg=ar_s3_helper&subdirectory=lib/python/ar_s3_helper'


# run the scanner - can be overriden when debugging.
CMD ["/opt/s3-delete.py"]
