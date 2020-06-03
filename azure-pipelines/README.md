## How To add a deployment to another AKS cluster

### Add deployment step

To add a step to edit the file `azure-pipelines/main.yaml` by adding a
stage that looks something like this (or just copy a similar step and edit):

```
  - stage: DeployNNN
    displayName: Deploy NNN
    dependsOn: Package
    condition: and(succeeded(), startsWith(variables['build.sourceBranch'], 'refs/tags/'))
    variables:
      - group: 'CLUSTER-NAME'
    jobs:
      - deployment: DeployMottak
        environment: 'CLUSTER-NAME'
        strategy:
          runOnce:
            deploy:
              steps:
                - template: deploy.yaml
                  parameters:
                    appName: 'mottak'
                    helmPackageArtifactName: 'mottak-helm-package'
                    helmReleaseName: 'mottak.mottak'
                    clusterName: 'CLUSTER-NAME'
                    azureResourceGroup: 'RESOURCE-GROUP'
                    namespace: ${{ variables.namespace }}
                    helmParameters: "\
                      tusd.mailgun_domain=\"$(tusdMailgunDomain)\",\
                      invitation.mailgun_domain=\"$(invitationMailgunDomain)\",\
                      invitation.upload_url=\"$(invitationUploadUrl)\""
```

Replace in `NNN` with something unique in the pipeline that makes sense for the cluster
(e.g. the cluster name in pascal-case). Replace `CLUSTER-NAME` with the name of the AKS cluster.
Replace `RESOURCE-GROUP` with the Azure resource group the cluster belongs to.

This stage will read the artifact left by the previous step, `Package`, called
`mottak-helm-package`. This is a Helm archive (basically a tarball of the Helm charts for the
application) that will be deployed to the AKS cluster named by `CLUSTER-NAME` and pass the
values of the variables found in the variable group named after the cluster.

The variable group and environment (a name Azure DevOps uses to track
historical data about a deployment) do not strictly speaking need to
have the same name as the cluster - it is only our convention since we
think these three things are strongly connected in our setup.

### Create a new variable group for the cluster

The apps in the cluster will need to have cluster-specific
configuration. The pipeline provides this by passing values from a
Azure Pipelines Variable Group to the Helm client during
deployment. These values aren't secret, but vary from one environment
to the next. Also, some of the values might be of a nature such that
we don't want them commited to source code viewable to everybody
(e.g. our mail gun domain).

If you have secrets (passwords, keys, etc.) do *not* put these in a
variable Group. Rather, put them in Azure Keyvault.

Since each cluster will need to provided (potentially) different
values, each cluster needs its own variable group. To create one, the
easiest way is to copy an existing variable group. To do this, go to
"Library" under "Pipelines" for the pipeline in question
(`arkivverket.mottak` for this repo). Point to the left of the "Date
modified" for three dots to appear (arguably not great UX). Then
choose "Clone" in the menu to make a copy of the variable group.

Edit the name, description and any variable *values* as
appropriate. It is also possible to edit/add variable names, but in
that case the corresponding stage in the pipeline must be changed to
reflect the changes made.


