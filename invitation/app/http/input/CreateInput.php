<?php

namespace app\http\input;

use mako\validator\input\HttpInput;

class CreateInput extends HttpInput
{
	protected $rules =
	[
		'name'            => ['required'],
		'email'           => ['required', 'email'],
		'uuid'            => ['required', 'uuid', 'unique("invitations","uuid")'],
		'checksum'        => ['required', 'exact_length(64)'],
		'archive_type_id' => ['required', 'exists("archive_types","id")'],
		'is_sensitive'    => ['required', 'in(["0","1"])'],
	];
}
