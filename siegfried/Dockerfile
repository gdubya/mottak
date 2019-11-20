FROM golang:1.12.0-alpine3.9
RUN mkdir -p /opt
COPY s3-siegfried.sh /opt
WORKDIR /opt
RUN go get github.com/richardlehane/siegfried/cmd/sf .
CMD ["sf -update"]
RUN apt-get update
RUN apt-get install -y s3cmd
# run the scanner - can be overriden when debugging.
CMD ["/opt/start.sh"]

