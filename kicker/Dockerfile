FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends python3 git wget
RUN mkdir -p /opt
RUN pip install poetry
# We don't need requirements.txt - we get native packages from debian.
# Install the helper module:
RUN useradd --home-dir /opt mol
WORKDIR /opt
COPY start.sh kicker.py pyproject.toml poetry.lock /opt/
RUN mkdir /opt/workflows
COPY workflows/*.yaml /opt/workflows/
RUN chown -R mol /opt
# USER mol
RUN poetry install

# install the Argo CLI
RUN wget -q https://github.com/argoproj/argo/releases/download/v2.8.0/argo-linux-amd64 && \
    chmod +x argo-linux-amd64 && \
    mv argo-linux-amd64 /usr/local/bin/argo

CMD ["/opt/start.sh"]
