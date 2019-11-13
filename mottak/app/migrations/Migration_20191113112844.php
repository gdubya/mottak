<?php

namespace app\migrations;

use mako\database\migrations\Migration;

class Migration_20191113112844 extends Migration
{
	/**
	 * Description.
	 *
	 * @var string
	 */
	protected $description = 'Create the base tables.';

	/**
	 * Makes changes to the database structure.
	 */
	public function up(): void
	{
		$this->getConnection()->query
		('
			CREATE TABLE "archive_types" (
				"id" SERIAL NOT NULL PRIMARY KEY,
				"created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
				"updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
				"type" VARCHAR(255) NOT NULL,
				"description" TEXT DEFAULT NULL
			)
		');

		$this->getConnection()->query('CREATE UNIQUE INDEX "idx_archive_types_type" ON "archive_types" ("type")');

		$this->getConnection()->query('INSERT INTO "archive_types" ("type", "created_at", "updated_at") VALUES (\'Noark-3\', NOW(), NOW())');
		$this->getConnection()->query('INSERT INTO "archive_types" ("type", "created_at", "updated_at") VALUES (\'Noark-4\', NOW(), NOW())');
		$this->getConnection()->query('INSERT INTO "archive_types" ("type", "created_at", "updated_at") VALUES (\'Noark-5\', NOW(), NOW())');

		$this->getConnection()->query
		('
			CREATE TABLE "invitations" (
				"id" SERIAL NOT NULL PRIMARY KEY,
				"created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
				"updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
				"archive_type_id" INTEGER NOT NULL REFERENCES "archive_types",
				"uuid" UUID NOT NULL,
				"checksum" CHAR(64) NOT NULL,
				"is_sensitive" BOOLEAN DEFAULT false NOT NULL,
				"name" VARCHAR(255) NOT NULL,
				"email" VARCHAR(255) NOT NULL
			)
		');

		$this->getConnection()->query('CREATE UNIQUE INDEX "idx_invitations_uuid" ON "invitations" ("uuid")');
	}

	/**
	 * Reverts the database changes.
	 */
	public function down(): void
	{
		$this->getConnection()->query('DROP TABLE "invitations"');

		$this->getConnection()->query('DROP TABLE "archive_types"');
	}
}
