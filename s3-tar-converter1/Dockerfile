FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get -y install software-properties-common && add-apt-repository ppa:libreoffice/ppa
RUN apt-get -y -q install gdb libreoffice libreoffice-writer ure \
    libreoffice-java-common libreoffice-core libreoffice-common openjdk-8-jre \
    fonts-opensymbol hyphen-fr hyphen-de hyphen-en-us hyphen-it hyphen-ru \
    fonts-dejavu fonts-dejavu-core fonts-dejavu-extra fonts-droid-fallback \
    fonts-dustin fonts-f500 fonts-fanwood fonts-freefont-ttf fonts-liberation \
    fonts-lmodern fonts-lyx fonts-sil-gentium fonts-texgyre fonts-tlwg-purisa
RUN apt-get -y -q remove libreoffice-gnome
RUN adduser --home=/home/libreoffice --disabled-password --gecos "" --shell=/bin/bash libreoffice
WORKDIR /opt/

# Python3:
RUN apt-get -y install python3 python3-pip git
COPY requirements.txt /opt/
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install -e 'git+https://github.com/arkivverket/mottak#egg=ar_s3_helper&subdirectory=lib/python/ar_s3_helper'

# Siegfried, which requires Go

RUN apt-get -y install golang-go

ENV PATH="/root/go/bin:${PATH}"
RUN go get github.com/richardlehane/siegfried/cmd/sf
RUN echo ${PATH}
RUN sf -update


# Application specifics
COPY start.sh /opt/
COPY pronomtypes.json /opt/
COPY s3-tar-converter1.py /opt/

# start up clamd and run the scanner - can be overriden when debugging.
CMD ["/opt/start.sh"]
