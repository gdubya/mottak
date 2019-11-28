Mailer


This container uses mailgun to send a single email. At the moment it looks at the following enviroment variables:
 - 'RECIPIENT'
 - 'SUBJECT'
 - 'MESSAGE'
 - 'MAILGUN_API_KEY'
 - 'MAILGUN_DOMAIN'

It logs to STDOUT.

Attached is also a tiny utility to look at the status of the last five messages sent.


Todo:
    - Take a reference to one or more files (argo artifacts) and attach them to the email
    - Take a longer message and use it for the body of the email



  