<?php

use mako\http\routing\Routes;

/* @var \mako\http\routing\Routes $routes */

$routes->group(['namespace' => 'app\http\controllers', 'middleware' => ['security_headers', 'input_validation']], function(Routes $routes): void
{
	$routes->get('/', 'Invitations::start', 'invitations.start');

	$routes->post('/', 'Invitations::parseXml');

	$routes->get('/create', 'Invitations::create', 'invitations.create');

	$routes->post('/create', 'Invitations::store');

	$routes->get('/receipt/{id}', 'Invitations::receipt', 'invitations.receipt')->patterns(['id' => '[0-9]+']);
});
