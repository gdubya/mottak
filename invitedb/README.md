
Database schema for the invitiation database.
Webform or XML-parser will populate the database with entries for invitations.

The service that axcepts the XML-schema or form will also send out an email to the creator with an URL for the uploader.


# Protocol
The application will be launched using the custom `dpldr` protocol. The link will consist of the protocol followed by a base64 enoded JSON payload:
```
dpldr://eyJmb2xkZXJOYW1lIjoxNTQzOTI1NDM2LCJ1cGxvYWRVcmwiOiJodHRwOlwvXC9leGFtcGxlLm9yZ1wvdXBsb2FkIiwibWV0YSI6eyJ1c2VySWQiOjEyMywidW5pdElkIjoxMjMsImZvbGRlck5hbWUiOjE1NDM5MjU0MzZ9fQ==
```
> Note that the protocol is `dpldrdev` when the application run in development mode.
The payload must contain the following data. Note that the meta block is optional (in this example it is specific for the Archive Digitisation application):
```
$data = [
	'reference'  => 'RA/EA-4070/Ki/L0009',       // (required) Name or reference that lets the user visually identify the upload in the client
	'uploadUrl'  => 'http://example.org/upload', // (required) URL to the tusd endpoint
	'uploadType' => 'directory',                 // (optional) Upload type. The allowed types are 'directory' and 'tar' (default: 'directory')
	'meta'       => [                            // (optional) Metadata that is sent back to the tusd server when the upload starts
		'userId'     => 123, // Value must be signed
		'unitId'     => 123, // Value must be signed
		'folderName' => 123, // Value must be signed
	],
];
```

