<?php

use mako\http\routing\Routes;

/* @var \mako\http\routing\Routes $routes */

$routes->group(['namespace' => 'app\http\controllers', 'middleware' => ['security_headers', 'input_validation']], function(Routes $routes): void
{
	$routes->get('/invitation/', 'Invitations::start', 'invitations.start');

	$routes->post('/invitation/', 'Invitations::parseXml');

	$routes->get('/invitation/create', 'Invitations::create', 'invitations.create');

	$routes->post('/invitation/create', 'Invitations::store');

	$routes->get('/invitation/receipt/{id}', 'Invitations::receipt', 'invitations.receipt')->patterns(['id' => '[0-9]+']);
});
