# mottak
a.k.a. Laks

Prototype application for recieving archives and processing them so they can later be put into storage.

The application allow someone to upload a Noark3 or Noark5 archieve into a s3-like objectstore and run some tests against it. The following tests are run:
 - checksum is matches against the expected checksum
 - the archieve is check for virus using ClamAV (note that clamAV doesn't seem to work against archieves larger than 4GB)
 - arkade5 is run against the archieve and it generates a report
 - if the archieve is processed successfully an email is sent

Requirements:
 - docker containers for each component.
 - Kubernetes with Argo for workflow processing
 - Postgresql for metadata for invitations
 - S3 or similar Objectstore for archieves

How to setup a new enviroment:
 - get a kubernetes cluster and make sure kubectl is operational
 - create a namespace: ```kubectl create name namespace argo```
 - install argo workflow into that namespace: https://github.com/argoproj/argo/blob/master/demo.md
 - test to make sure the argo installation works.
 - Load the secrets, some guidance is found in k8s/load-secrets. You need the following secrets to be set:
   - dns-cred     # for external-dns
   - dsn          # database access string
   - gcs-cred     # Google cloud storage for tusd (the S3 APIs don't work for tusd, yet)
   - invitation   # the string needed for xss protection on the invitation app
   - mailgun      # mailgun API key and domain. we use mailgun for mail
   - s3-cret      # s3 keys for the python containers
 - go into the k8s folder and ```cp patches-template.yaml patches.yaml```
 - edit patches.yaml to suit your needs
 - edit k8s/argo/argo-artifacts.yaml (make sure you replace all the namespace references)
 - deploy (still in the k8s folder):
   - ```kubectl apply -k .```


At this point everything should work.


You can view the Argo UI by setting up a kube proxy:

kubectl -n argo port-forward deployment/argo-ui 8001:8001

Then visit http://localhost:8001/ to view the UI.
