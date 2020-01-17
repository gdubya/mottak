# Mottak

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