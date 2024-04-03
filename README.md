# Setting Up a Multi-Master Kubernetes Cluster with Kubeadm on CentOS

## Introduction
This guide details the process for setting up a high-availability Kubernetes cluster using Kubeadm on CentOS servers. It is adapted from [Setup a multi-master Kubernetes cluster with kubeadm](https://github.com/tranductrinh/k8s/blob/main/create-ha-cluster/README.md) but tailored for CentOS servers and assumes root user access.

## Cluster Configuration
- **Masters**: 3 nodes, each with 2 CPUs and 2 GB RAM
- **Workers**: 3 nodes, each with 2 CPUs and 2 GB RAM
- **Load Balancers**: 2 nodes, each with 1 CPU and 1 GB RAM

![Cluster Setup Diagram](setup.png "Cluster Setup Diagram")

## Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/lethanhson9901/k8s-centos-ha-clusters
   cd k8s-centos-ha-clusters
   sudo su
   chmod +x ./* # Grant execution access to shell scripts
   ./install_vq.sh #install vq to read yml file
   ```

## Setting Up Load Balancers
1. Modify `lb_config.yml` to configure the IP addresses of your load balancers:
   ```bash
   nano config/lb_config.yml
   ```
2. Run the setup script on each load balancer node:
   ```bash
   ./setup_lb.sh
   ```
3. Verify the HAProxy service status:
   ```bash
   systemctl status haproxy
   ```

## Setting Up Kubernetes Cluster
1. Modify `cluster_config.yml` to list the IP addresses of master and worker nodes:
   ```bash
   nano config/cluster_config.yml
   ```
2. Execute the setup script on each master and worker node to install Kubeadm, Containerd, and other dependencies:
   ```bash
   ./install_kubeadm_containerd.sh
   ```
3. In case of errors, you can reverse the setup by running:
   ```bash
   ./cleanup.sh
   ```
## Setting Up Kubernetes Cluster (Continued)

1. Initializing the First Master Node

    After modifying the `cluster_config.yml` and executing the setup scripts, the next step is to initialize the first master node in the Kubernetes cluster.

2. Choose a CNI Plugin
    - **Options**: Choose a Container Network Interface (CNI) such as Calico, Flannel, etc., for network operations in your Kubernetes cluster.
    - **Documentation**: For more information, visit [Kubernetes CNI plugins documentation](https://kubernetes.io/docs/concepts/cluster-administration/networking/).

3. Initialize with Flannel
    - If you opt for Flannel as your CNI, use `10.244.0.0/16` as the `pod-network-cidr`.
    - **Initialization Command**:
    ```bash
    kubeadm init --control-plane-endpoint "<cluster-vip-ip>:6443" --pod-network-cidr="10.244.0.0/16"
    ```
    Replace `<cluster-vip-ip>` with the virtual IP address of your cluster.

4. Set Up Kubeconfig
    - After initializing the first master node, configure kubeconfig to manage your Kubernetes cluster:
    ```bash
    mkdir -p $HOME/.kube
    sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config
    ```

5. Verify the Setup
    - Check the setup by listing all pods in the `kube-system` namespace:
    ```bash
    kubectl get pods --namespace=kube-system
    ```

## Installing the CNI Plugin

After the first master node initialization, the next crucial step is to install the selected CNI plugin.

1. Install Flannel CNI
- **Apply Flannel Configuration**: Download and apply the Flannel configuration to your Kubernetes cluster.
  ```bash
  kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
  systemctl restart containerd
  ```
- **Check Installation**: Confirm the deployment of Flannel.
  ```bash
  kubectl get pods --namespace=kube-system
  ```
  Look for `kube-flannel-ds` pods in the `Running` state.

2. Verify Node Network
- Ensure each node is `ready`` and communicating correctly:
  ```bash
  kubectl get nodes
  ```

3. Notes
- **Network Configuration**: By default, Flannel uses the `10.244.0.0/16` subnet.
- **Compatibility**: Ensure there are no conflicts with existing network infrastructures.
- **Alternatives**: If you prefer a different CNI, use the respective configuration file URL for installation.

Following these steps will ensure the successful installation of Flannel as your Kubernetes cluster's CNI, enabling seamless pod-to-pod networking.

## Join Other Master Nodes

#### Steps:
1. **Use the `kubeadm join` command** from the initial master node's output. Replace the tokens and addresses with your specific details. Example:
   ```bash
   kubeadm join <cluster-vip-ip>:6443 --token <token> \
    --discovery-token-ca-cert-hash sha256:<hash> \
    --control-plane --certificate-key <certificate-key> --apiserver-advertise-address <master-ip>
   ```

2. **Set up kubeconfig** (Repeat on each master node):
   ```bash
   mkdir -p $HOME/.kube
   sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
   sudo chown $(id -u):$(id -g) $HOME/.kube/config
   ```
3. (Optional) Incase token is expired or you forgot:
    **Recreate Token if Needed**:
   ```bash
   kubeadm token create --print-join-command
   kubeadm init phase upload-certs --upload-certs
   ```

4. **In case errors**: reset kubeadm
   ```
   kubeadm reset -f
   rm -rf /var/lib/kubelet/* /etc/kubernetes/* /var/lib/containerd/* /etc/cni/net.d/* /var/log/containers/* /var/log/pods/*
   ```

## Join Worker Nodes

#### Steps:
1. **Use `kubeadm join` command** for worker nodes (similar to master nodes but without `--control-plane` and `--certificate-key` flags):
   ```bash
   kubeadm join <cluster-vip-ip>:6443 --token <token> \
    --discovery-token-ca-cert-hash sha256:<hash>
   ```

### Verifying the Cluster

- **Run the following commands** to verify the cluster setup:
  ```bash
  kubectl cluster-info
  kubectl get nodes
  kubectl get cs
  ```

## Additional Setup

### Kuberbetes Dashboard UI

[Deploy and Access the Kubernetes Dashboard](son_namespace/dashboard/README.md)

### Chaos Engineering with Chaos Mesh

After setting up your high-availability Kubernetes cluster, you might want to test its resilience against various types of failures. Chaos Mesh is an open-source chaos engineering platform that helps you simulate system conditions and find potential issues in your deployment.

#### Installing Chaos Mesh

To install Chaos Mesh in your Kubernetes cluster, refer to the detailed guide provided in the [Chaos Mesh README](son_namespace/chaos-mesh/README.md). This guide covers the steps for adding the Chaos Mesh Helm repository, creating a namespace for Chaos Mesh, installing Chaos Mesh using Helm, and verifying the installation.

#### Exploring Chaos Mesh

Once installed, you can begin experimenting with Chaos Mesh by creating chaos experiments. These experiments help you understand how your cluster responds to various failure scenarios, enabling you to improve its resilience.

For more detailed instructions on installing and using Chaos Mesh, including setting up chaos experiments, please refer to the [Chaos Mesh README](son_namespace/chaos-mesh/README.md).

### [Storage Plug-in](son_namespace/storage/README.md)

- [NFS File Storage](son_namespace/nfs-server/README.md)
- [Ceph Storage](son_namespace/storage/rook-ceph/README.md)

### [Databases](son_namespace/db)

- [InfluxDB](son_namespace/db/influxdb/v2/README.md)
- [PostgresDB](son_namespace/db/postgres/cnpg/README.md)
- [MongoDB](son_namespace/db/mongodb/internal)

### Basic Application

- [NGINX Ingress Controller Setup Guide](son_namespace/nginx-ingress/README.md)

### Setup CI/CD pipeline

- [CI/CD pipeline with Jenkins, Gitlab, Sonarqube](son_namespace/deploy/jenkins-gitlab-sonarqube-pg-docker/README.md)

### Microservice in Kubernetes

- [Setting Up Django with Kubernetes: A Microservices Architecture Guide](son_namespace/deploy/istio/django-kubernetes-service1)

- [Kafka Microservices Deployment Guide](son_namespace/deploy/python-kafka-microservice/README.md)

Enjoy your Kubernetes Cluster!
