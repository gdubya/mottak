# Mottak

## Setup

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

Run the migrations using the following command:

```
php app/reactor migrate.up
```