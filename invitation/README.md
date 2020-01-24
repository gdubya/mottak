# Mottak

invitation creates a friendly web ui that allows you to upload a
an XML document created by Arkade5. It will parse the XML file and fill out a webform that will allow you to invite someone to upload an archieve.

After uploading the XML the form is partially filled out. You fill out the rest and the uploader will get an email with a link.

The link is a base64 encoded JSON doc. Se "build-upload-url.py" in the tusd folder on how to build an URL.

The user must have the uploader program installed.


It is meant to run in a Docker container. All configuration should be dynamic. It relies on the following envirment variables being set:
 * UPLOAD_URL: The URL of your tusd upload target.
 * APPLICATION_SECRET: The secret used to protect the forms from XSS
 * DBSTRING: database configuration. 
 * MAILGUN_API_KEY: API key for mailgun
 * MAILGUN_DOMAIN: Your mailgun domain




Todo:
 * The invite mail (sent through mailgun) needs templating.
 * The URL should be signed (through HMAC or similar) and the uploader should verify this signature. The tusd-hook should also verify this signature.


## Setup

### Database

 - CREATE USER invitation WITH PASSWORD 'REDACTED';
 - CREATE SCHEMA invitation
 - GRANT ALL PRIVILEGES ON SCHEMA invitation TO invitation
  

### Web application
Install dependencies using [composer](https://packagist.org) by running the following command:

```
composer install
```

Create the migrations table:

```
CREATE TABLE "mako_migrations"
(
	"batch" BIGINT NOT NULL,
	"version" TEXT NOT NULL,
	"package" TEXT
);
```

now create the DSN. Either have it be set by k8s (when running in k8s) or set up a .env file with the enviroment variable DSN.

Run the migrations using the following command:

```
php app/reactor migrate.up
```