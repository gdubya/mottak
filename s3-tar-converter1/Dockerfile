FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get -y --no-install-recommends install software-properties-common && \
    add-apt-repository ppa:libreoffice/ppa && \
    apt-add-repository multiverse
RUN apt-get -y --no-install-recommends -q install libreoffice libreoffice-writer \
    libreoffice-java-common default-jre \
    fonts-opensymbol hyphen-no hyphen-en-us hyphen-it \
    fonts-dejavu fonts-dejavu-core fonts-dejavu-extra fonts-droid-fallback \
    fonts-dustin fonts-f500 fonts-fanwood fonts-freefont-ttf fonts-liberation \
    fonts-lmodern fonts-lyx fonts-sil-gentium fonts-texgyre fonts-tlwg-purisa

# MS Core Fonts:

RUN echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections
RUN apt-get install -y --no-install-recommends fontconfig ttf-mscorefonts-installer
COPY localfonts.conf /etc/fonts/local.conf
RUN fc-cache -f -v

RUN adduser --home=/home/libreoffice --disabled-password --gecos "" --shell=/bin/bash libreoffice
WORKDIR /opt/

# Python3:
RUN apt-get -y --no-install-recommends install python3 python3-pip git python3-setuptools
COPY requirements.txt /opt/
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install -e 'git+https://github.com/arkivverket/mottak#egg=av_objectstore&subdirectory=lib/python/av_objectstore'

# Siegfried, which requires Go

RUN apt-get -y --no-install-recommends install golang-go

ENV PATH="/root/go/bin:${PATH}"
RUN go get github.com/richardlehane/siegfried/cmd/sf
RUN echo ${PATH}
RUN sf -update


# Application specifics
COPY start.sh /opt/
COPY pronomtypes.json /opt/
COPY s3-tar-converter1.py /opt/


# TODO
# test.exec_run('libreoffice --headless --cat "test"', user='libreoffice')

# start up clamd and run the scanner - can be overriden when debugging.
CMD ["/opt/start.sh"]
