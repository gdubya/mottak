<?php

namespace app\console\commands;

use mako\database\ConnectionManager;
use mako\reactor\Command;

/**
 * Setup command.
 */
class Setup extends Command
{
	/**
	 * {@inheritdoc}
	 */
	protected $description = 'Sets up the migration table.';

	/**
	 * Setup.
	 *
	 * @param \mako\database\ConnectionManager $database Connection manager
	 * @return void
	 */
	public function execute(ConnectionManager $database): void
	{
		$database->connection()->query
		('
			CREATE TABLE IF NOT EXISTS "mako_migrations"
			(
				"batch" BIGINT NOT NULL,
				"version" TEXT NOT NULL,
				"package" TEXT
			)
		');
	}
}
