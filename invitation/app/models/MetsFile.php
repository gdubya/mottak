<?php

namespace app\models;

use mako\database\midgard\ORM;
use mako\database\midgard\relations\BelongsTo;
use mako\database\midgard\traits\TimestampedTrait;

class MetsFile extends ORM
{
	use TimestampedTrait;

	public function archiveType(): BelongsTo
	{
		return $this->BelongsTo(Invitation::class);
	}
}
