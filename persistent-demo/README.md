Just a persistent service running in the same k8s cluster as Argo.

We'll put these services in a separate namespare ("mottak") to make sure they don't collide with argo.

Here are some notes on how this is set up. 
```
 $ kubectl create namespace mottak
```

To make this the default for kubectl:
```
kubectl config set-context $(kubectl config current-context) --namespace mottak
```

to change back to argo just replace mottak with argo in the previous command.

Hello World:

to deploy:
 - kubectl apply -f hello-world-pod.yaml

Now set up load balancing:
 - kubectl apply -f service.yaml

Inspect state:
 - kubectl get services

To delete these pods and services just do the following:
 - kubectl delete -f service.yaml
 - kubectl delete -f hello-world-pod.yaml

