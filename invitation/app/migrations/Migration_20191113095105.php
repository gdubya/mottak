<?php

namespace app\migrations;

use mako\database\migrations\Migration;

class Migration_20191113095105 extends Migration
{
	/**
	 * Description.
	 *
	 * @var string
	 */
	protected $description = 'Create gatekeeper tables.';

	/**
	 * Makes changes to the database structure.
	 */
	public function up(): void
	{
		$this->getConnection()->query
		('
			CREATE TABLE "users" (
			"id" SERIAL NOT NULL PRIMARY KEY,
			"created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
			"updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
			"ip" VARCHAR(255) NOT NULL,
			"username" VARCHAR(255) NOT NULL UNIQUE,
			"email" VARCHAR(255) NOT NULL UNIQUE,
			"password" VARCHAR(255) NOT NULL,
			"action_token" CHAR(64) DEFAULT \'\',
			"access_token" CHAR(64) DEFAULT \'\',
			"activated" BOOLEAN NOT NULL DEFAULT FALSE,
			"banned" BOOLEAN NOT NULL DEFAULT FALSE,
			"failed_attempts" INTEGER NOT NULL DEFAULT 0,
			"last_fail_at" TIMESTAMP(0) WITHOUT TIME ZONE DEFAULT NULL,
			"locked_until" TIMESTAMP(0) WITHOUT TIME ZONE DEFAULT NULL
			)
		');

		$this->getConnection()->query
		('
			CREATE TABLE "groups" (
				"id" SERIAL NOT NULL PRIMARY KEY,
				"created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
				"updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
				"name" VARCHAR(255) NOT NULL UNIQUE
			)
		');

		$this->getConnection()->query
		('
			CREATE TABLE "groups_users" (
				"group_id" INTEGER NOT NULL REFERENCES "groups" ON DELETE CASCADE,
				"user_id" INTEGER NOT NULL REFERENCES "users" ON DELETE CASCADE,
				UNIQUE ("group_id", "user_id")
			)
		');

		$this->getConnection()->query
		('
			CREATE INDEX "groups_users_group_id_idx" ON "groups_users" USING btree("group_id")
		');

		$this->getConnection()->query
		('
			CREATE INDEX "groups_users_user_id_idx" ON "groups_users" USING btree("user_id")
		');
	}

	/**
	 * Reverts the database changes.
	 */
	public function down(): void
	{
		$this->getConnection()->query('DROP TABLE "groups_users"');

		$this->getConnection()->query('DROP TABLE "groups"');

		$this->getConnection()->query('DROP TABLE "users"');
	}
}
