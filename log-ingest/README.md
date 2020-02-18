# Log-ingest/query 


To get it up and running do the following.


- Create a database schema called "log".
  - CREATE USER LOG WITH PASSWORD 'REDACTED'
  - GRANT ALL PRIVILEGES ON SCHEMA log TO log;
- pip install -f requirements.txt
- pip install yoyo-migrations
- yoyo apply --database 'postgresql://log:REDACTED@REDACTED/postgres' ./migrations
  - Note that this will create a yoyo.ini which stores the database password in clear text.
  - set DSN env var.

This will create the relations in the database. Now run the tests:
- pytest

Once the test run nicely run the server.
- uvicorn main:app --reload

