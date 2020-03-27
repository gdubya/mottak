# Infrastructure as Code for Mottak


## High level overview. Separation of concerns.

We use three tools to roll out our infrastructure and applications. 
 - Terraform
 - Helm
 - Kubernetes

These are general guidelines. Sometimes we might need to do things in the "wrong" place. For instance, if a Kubernetes Pod might need file storage from Azure it might make sense for the pod to acquire it itself.

## Terraform

Terraform is responsible for acquiring the infrastructure components we need. So it might provision things like:
 - Kubernetes clusters
 - Virtual machines
 - Storage (blob and file)
 - Databases

These are more or less static resources if we disregard things like scaling and growing of resources.

### Terraform state

Terraform needs to keep state somewhere. We use Azure Blob Storage. 

## Helm

Helm is responsible for populating namespaces in Kubernetes with content. So, in order to provision an application you might need to create a namespace in Kubernetes and point Helm at it to fill it with something.


## Documentation resources:
 - Terraform docs: https://www.terraform.io/docs/index.html
 - Azure Provider: https://www.terraform.io/docs/providers/azurerm/index.html


## Getting started

To create a new Kubernetes cluster run the command:

    ./create-cluster --subscription ...

And follow the instructions given.

The subscription is necessary if you have more than one subscription id.

## Terraform

Once you are up and running you will likely iterate in more or less this fashion:

 - terraform plan
 - terraform apply
 - when things work - git commit

