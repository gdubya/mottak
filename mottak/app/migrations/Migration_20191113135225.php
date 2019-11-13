<?php

namespace app\migrations;

use mako\database\migrations\Migration;

class Migration_20191113135225 extends Migration
{
	/**
	 * Description.
	 *
	 * @var string
	 */
	protected $description = 'Add "is_uploaded" column to "invitations" table.';

	/**
	 * Makes changes to the database structure.
	 */
	public function up(): void
	{
		$this->getConnection()->query
		('
			ALTER TABLE "invitations"
			ADD COLUMN "is_uploaded" BOOLEAN DEFAULT false NOT NULL
		');
	}

	/**
	 * Reverts the database changes.
	 */
	public function down(): void
	{
		$this->getConnection()->query
		('
			ALTER TABLE "invitations"
			DROP COLUMN "is_uploaded"
		');
	}
}
