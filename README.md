# mottak
a.k.a. Laks

Prototype application for recieving archives and processing them.

Requirements:
 - docker containers for each component.
 - Kubernetes with Argo for workflow processing
 - Postgresql for metadata for invitations
 - S3 Objectstore for archieves

The easiest way of building the containers is through Google Cloud Builder - which uses cloudbuild.yaml

Build everything and pubish the resulting images to a container repo.

Edit the k8s deployment files and make sure they reference the correct images.

You want two pods running, tusd and invitation.

Then install argo into the argo namespace. Make sure tusd can submit workflows.

