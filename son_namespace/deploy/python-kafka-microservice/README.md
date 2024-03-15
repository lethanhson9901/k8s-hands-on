# Kafka Microservices Deployment Guide

## Introduction
This guide provides detailed instructions on deploying a Kafka cluster, microservices for order processing, transactions, notifications, and analytics, and setting up Kafka UI in a Kubernetes environment. The setup uses Helm charts for Kafka and Kafka UI, and kubectl commands to deploy services in a specified namespace.

To clarify the process more visually and straightforwardly, let's break down the flow into a simple sequence of steps and actions:

1. **Generate Orders**:
    - Create fake order data.
    - Publish to Kafka topic: `order-details`.

2. **Process Orders**:
    - Consume from `order-details`.
    - Calculate total cost.
    - Publish processed data to: `order-processed`.

3. **Email Notification** (optional path):
    - Consume from `order-processed`.
    - Extract customer email.
    - Simulate sending email.

4. **Analytics Update** (optional path):
    - Consume from `order-processed`.
    - Update total orders and revenue metrics.

**Visual Flow**:

```
Step 1: [Generate Orders] ---> Publish to ---> [Kafka Topic: order-details]

Step 2: [Consume from order-details] ---> [Process Orders] ---> Publish to ---> [Kafka Topic: order-processed]

Step 3a: [Consume from order-processed] ---> [Email Notification] ---> Simulate Email Sending

OR

Step 3b: [Consume from order-processed] ---> [Analytics Update] ---> Log Metrics
```

This flow highlights the linear progression from generating orders to processing them and then branching into either notifying customers via email or updating analytics based on the processed orders. Each step is dependent on Kafka topics for message passing, demonstrating a clear separation of concerns and modular architecture.

## Prerequisites
- Kubernetes cluster
- Helm 3
- kubectl configured to interact with your Kubernetes cluster

## Installation

### Deploying Kafka Cluster
To deploy a Kafka cluster without persistence (ideal for development or testing), use the following Helm commands:

1. Add the Bitnami Helm repository:
   ```shell
   helm repo add bitnami https://charts.bitnami.com/bitnami
   ```
2. Install the Kafka chart with persistence disabled for both Kafka and Zookeeper:
   ```shell
   helm install kafka-local bitnami/kafka \
   --set persistence.enabled=false,zookeeper.persistence.enabled=false
   ```

### Setting Up Kafka Client
To interact with the Kafka cluster, deploy a temporary Kafka client:
```shell
kubectl run kafka-local-client \
    --restart='Never' \
    --image docker.io/bitnami/kafka:3.3.1-debian-11-r19 \
    --namespace orders-microservice \
    --command \
    -- sleep infinity
```
Access the client shell:
```shell
kubectl exec --tty -i kafka-local-client --namespace orders-microservice -- bash
```

## Service Deployment
Deploy microservices related to orders, transactions, notifications, and analytics using kubectl commands:

### Order Service
```shell
kubectl run order-svc --rm --tty -i \
    --image worldbosskafka/orders:v1.0.0 \
    --restart Never \
    --namespace orders-microservice \
    --command \
    -- python3 -u ./order_svc.py
```

### Transaction Service
```shell
kubectl run transaction-svc --rm --tty -i \
    --image worldbosskafka/transactions:v1.0.0 \
    --restart Never \
    --namespace orders-microservice \
    --command \
    -- python3 -u ./transaction.py
```

### Notification Service
```shell
kubectl run notification-svc --rm --tty -i \
    --image worldbosskafka/notification:v1.0.0 \
    --restart Never \
    --namespace orders-microservice \
    --command \
    -- python3 -u ./notification.py
```

### Analytics Service
```shell
kubectl run analytics-svc --rm --tty -i \
    --image worldbosskafka/analytics:v1.0.0 \
    --restart Never \
    --namespace orders-microservice \
    --command \
    -- python3 -u ./analytics.py
```

## Kafka UI Setup
To visualize and manage your Kafka cluster, deploy Kafka UI:

1. Add the Kafka UI Helm repository:
   ```shell
   helm repo add kafka-ui https://provectus.github.io/kafka-ui
   ```
2. Install Kafka UI connected to your Kafka cluster:
   ```shell
   helm install kafka-ui kafka-ui/kafka-ui \
   --set envs.config.KAFKA_CLUSTERS_0_NAME=kafka-local \
   --set envs.config.KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=kafka-local.orders-microservice.svc.cluster.local:9092
   ```
3. Access Kafka UI by forwarding the port:
   ```shell
   kubectl port-forward svc/kafka-ui 8080:8080
   ```
   Visit `http://localhost:8080` in your web browser to access the Kafka UI dashboard.

## Conclusion
Following these instructions will set up a Kafka cluster, deploy essential microservices for a typical order processing system, and enable Kafka UI for cluster management and monitoring. This setup is designed for development and testing environments, emphasizing ease of deployment and configuration.
