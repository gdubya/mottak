FROM mcr.microsoft.com/dotnet/core/runtime:3.1.1-buster-slim
RUN mkdir -p /opt
WORKDIR /opt
RUN apt-get update && apt-get install -y --no-install-recommends wget unzip lsb-release curl gnupg2
RUN wget https://github.com/arkivverket/arkade5/releases/download/v1.5.1/Arkade5CLI-1.5.1.zip
RUN unzip Arkade5CLI-1.5.1.zip
RUN chmod +x /opt/Arkade5CLI-1.5.1/arkade.sh

# Get GCS-fuse
# If we need to support other clouds we need to add their respective FUSE drivers.
RUN export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s` && \
    echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | tee /etc/apt/sources.list.d/gcsfuse.list && \
    curl --output - https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && apt-get install -y --no-install-recommends gcsfuse

# While developing we use this.
COPY gcs.json /etc/gcs/gcs.json
COPY get-mets.py /opt
COPY run.sh /opt
CMD ["/opt/run.sh"]
