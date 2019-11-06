FROM mcr.microsoft.com/dotnet/core/runtime:3.0-bionic
RUN mkdir -p /opt
WORKDIR /opt
COPY start.sh /opt
RUN apt-get update
RUN apt-get install -y wget unzip s3cmd
RUN wget https://github.com/arkivverket/arkade5/releases/download/v1.5.0/Arkade5CLI-1.5.0.zip
RUN unzip Arkade5CLI-1.5.0.zip
RUN chmod +x /opt/Arkade5CLI-1.5.0/arkade.sh
CMD ["/opt/start.sh"]