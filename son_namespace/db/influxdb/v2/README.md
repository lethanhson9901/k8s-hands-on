# Kubernetes InfluxDB & Telegraf Deployment

## Overview

This README provides detailed instructions on deploying InfluxDB 2 and Telegraf within a Kubernetes cluster using Helm. The deployment focuses on persistence for InfluxDB and integrates Telegraf as a metrics collector.

## Prerequisites

- A Kubernetes cluster
- Helm 3 installed
- Access to your Kubernetes cluster configuration

## Deploying InfluxDB 2

### Installation

To install InfluxDB 2 as a StatefulSet in your Kubernetes cluster, use the following Helm command:

```shell
helm upgrade --install influxdb2-release -f values.yaml influxdata/influxdb2
```

Ensure your `values.yaml` file specifies necessary configurations such as persistence settings, resource allocations, and any custom configurations tailored to your environment.

Now pvc `influxdb2-release` is pending beacause no persistent volumes available for this claim and no storage class is set. 

```shell
(base) [root@k8s-master-1 v2]# k get pvc
NAME                STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
influxdb2-release   Pending                                                     <unset>                 11s
(base) [root@k8s-master-1 v2]# k describe pvc influxdb2-release
Name:          influxdb2-release
Namespace:     default
StorageClass:  
Status:        Pending
Volume:        
Labels:        app.kubernetes.io/instance=influxdb2-release
               app.kubernetes.io/managed-by=Helm
               app.kubernetes.io/name=influxdb2
               app.kubernetes.io/version=2.7.4
               helm.sh/chart=influxdb2-2.1.2
Annotations:   helm.sh/resource-policy: keep
               meta.helm.sh/release-name: influxdb2-release
               meta.helm.sh/release-namespace: default
Finalizers:    [kubernetes.io/pvc-protection]
Capacity:      
Access Modes:  
VolumeMode:    Filesystem
Used By:       influxdb2-release-0
Events:
  Type    Reason         Age                   From                         Message
  ----    ------         ----                  ----                         -------
  Normal  FailedBinding  13s (x11 over 2m30s)  persistentvolume-controller  no persistent volumes available for this claim and no storage class is set

```

To allow dynamic provisioning using Ceph Storage Class `rook-ceph-block`:


```shell
kubectl apply -f ceph-sc.yaml
```

### Access and Configuration

Retrieve the admin password for InfluxDB 2 with:

```shell
echo $(kubectl get secret influxdb2-release-influxdb2-auth -o "jsonpath={.data['admin-password']}" --namespace default | base64 --decode)
```

**Note:** The admin password is set during the initial deployment. It's crucial to store this password securely.

### Persistence

InfluxDB 2 utilizes PersistentVolumeClaims (PVCs) to ensure data persists across pod restarts and deployments. The deployment script automatically configures a PVC.

Verify the PVC status:

```shell
kubectl get pvc influxdb2-release-influxdb2
```

## Deploying Telegraf

### Installation

Deploy Telegraf within the same Kubernetes cluster and namespace, ensuring it's configured to collect metrics from desired sources and forward them to InfluxDB 2.

```shell
helm upgrade --install telegraf-release \
  --set persistence.enabled=true \
    influxdata/telegraf
```

### Access and Management

To open a shell session in the container running Telegraf:

```shell
kubectl exec -i -t --namespace default $(kubectl get pods --namespace default -l app.kubernetes.io/name=telegraf-release-telegraf -o jsonpath='{.items[0].metadata.name}') /bin/sh
```

To view Telegraf pod logs:

```shell
kubectl logs -f --namespace default $(kubectl get pods --namespace default -l app.kubernetes.io/name=telegraf-release-telegraf -o jsonpath='{ .items[0].metadata.name }')
```

## Maintenance and Support

Regular maintenance tasks may include checking pod statuses, updating Helm charts, and monitoring resource usage. Ensure you follow best practices for securing and backing up your data.

## Troubleshooting

- If you encounter issues with PVC binding, verify the PersistentVolume and StorageClass configurations.
- For Helm deployment issues, use `helm list` and `helm status telegraf-release` to investigate the deployed resources and their statuses.

---

https://docs.influxdata.com/platform/install-and-deploy/deploying/kubernetes/