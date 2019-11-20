<?php

namespace app\http\input;

use mako\validator\input\HttpInput;

class XmlInput extends HttpInput
{
	protected $shouldIncludeOldInput = false;

	protected $rules =
	[
		'archive' => ['required', 'is_uploaded', 'mime_type(["application/xml", "text/xml"])'],
	];

	public function getInput(): array
	{
		return $this->request->getFiles()->all();
	}
}
