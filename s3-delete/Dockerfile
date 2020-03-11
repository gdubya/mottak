FROM python:3.8-slim-buster
RUN apt-get update && apt-get install -y --no-install-recommends python3 git && apt-get clean
RUN mkdir -p /opt
WORKDIR /opt
COPY s3-delete.py pyproject.toml poetry.lock /opt/
RUN pip install poetry
RUN poetry install
# run the scanner - can be overriden when debugging.
CMD ["poetry", "run", "/opt/s3-delete.py"]
