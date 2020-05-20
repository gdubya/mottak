<?php

namespace app\http\controllers;

use mako\http\response\builders\JSON;
use mako\http\response\senders\Stream;
use mako\http\routing\Controller;

/**
 *
 */
class LogProxy extends Controller
{
	/**
 	 *
 	 */
	public function view(string $uuid): JSON
	{

	}

	/**
 	 *
 	 */
	public function attachment(int $id): Stream
	{

	}
}
