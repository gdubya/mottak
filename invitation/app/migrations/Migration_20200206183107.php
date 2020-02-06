<?php

namespace app\migrations;

use mako\database\migrations\Migration;

class Migration_20200206183107 extends Migration
{
	/**
	 * Description.
	 *
	 * @var string
	 */
	protected $description = 'Creates the "mets_files" table.';

	/**
	 * Makes changes to the database structure.
	 */
	public function up(): void
	{
		$this->getConnection()->query
		('
			CREATE TABLE "mets_files" (
				"id" SERIAL NOT NULL PRIMARY KEY,
				"created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
				"updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
				"invitation_id" INTEGER NOT NULL REFERENCES "invitations",
				"contents" XML NOT NULL,
				UNIQUE ("invitation_id")
			)
		');
	}

	/**
	 * Reverts the database changes.
	 */
	public function down(): void
	{
		$this->getConnection()->query
		('
			DROP TABLE "mets_files"
		');
	}
}
