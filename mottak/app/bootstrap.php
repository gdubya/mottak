<?php

// This file gets included at the end of the application boot sequence

use Symfony\Component\Dotenv\Dotenv;

if($app->getEnvironment() === 'dev')
{
	$env = new Dotenv;

	$env->load(dirname(__DIR__) . '/.env');
}
