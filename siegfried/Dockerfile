FROM golang:1.12.0-alpine3.9
RUN mkdir -p /opt
RUN apk add --no-cache git
RUN  apk add --no-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ s3cmd
COPY start.sh /opt
WORKDIR /go
RUN go get github.com/richardlehane/siegfried/cmd/sf
RUN sf -update
# CMD ["sf -update"]
# run the scanner - can be overriden when debugging.
CMD ["/opt/start.sh"]

