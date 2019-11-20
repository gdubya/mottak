<?php

return
[
	'default' => 'cloudsql',

	'configurations' =>
	[
		'cloudsql' =>
		[
			'dsn'         => 'pgsql:dbname=mottak;host=' . getenv('DB_HOST') . ';port=5432;options=\'--client_encoding=UTF-8\'',
			'username'    => getenv('DB_USER'),
			'password'    => getenv('DB_PASSWORD'),
			'persistent'  => false,
			'log_queries' => true,
		],
	],
];
