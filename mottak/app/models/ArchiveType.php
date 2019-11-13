<?php

namespace app\models;

use mako\database\midgard\ORM;
use mako\database\midgard\relations\HasMany;
use mako\database\midgard\traits\TimestampedTrait;

class ArchiveType extends ORM
{
	use TimestampedTrait;

	public function invitations(): HasMany
	{
		return $this->hasMany(Invitation::class);
	}
}
