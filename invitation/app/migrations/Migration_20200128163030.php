<?php

namespace app\migrations;

use mako\database\migrations\Migration;

class Migration_20200128163030 extends Migration
{
	/**
	 * Description.
	 *
	 * @var string
	 */
	protected $description = 'Add "object_name" column to "invitations" table.';

	/**
	 * Makes changes to the database structure.
	 */
	public function up(): void
	{
		$this->getConnection()->query
		('
			ALTER TABLE "invitations"
			ADD COLUMN "object_name" VARCHAR (256)
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
			DROP COLUMN "object_name"
		');
	}
}
