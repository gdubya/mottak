FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends python3 git
RUN mkdir -p /opt
RUN pip install poetry
# We don't need requirements.txt - we get native packages from debian.
# Install the helper module:
RUN useradd --home-dir /opt mol
WORKDIR /opt
COPY kicker.py pyproject.toml poetry.lock /opt/
RUN chown -R mol /opt
USER mol
RUN poetry install
CMD ["/usr/local/bin/poetry", "run", "/opt/kicker.py"]
