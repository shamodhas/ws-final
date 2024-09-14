#!/bin/bash

# Apply Kubernetes manifests
kubectl apply -f account-service/k8s/
kubectl apply -f trade-service/k8s/
kubectl apply -f user-service/k8s/

# Wait for deployments to complete
kubectl rollout status deployment/account-service
kubectl rollout status deployment/trade-service
kubectl rollout status deployment/user-service
