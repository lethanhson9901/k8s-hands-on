# Kubernetes Dashboard Admin User Setup

This guide outlines the process for creating a new user with admin permissions in Kubernetes, granting access to the Kubernetes Dashboard using a bearer token. The setup involves creating a Service Account, a ClusterRoleBinding, and optionally, a Secret for a long-lived token.

## Prerequisites

- A Kubernetes cluster with the Dashboard deployed.
- `kubectl` configured to communicate with your cluster.

## Configuration Steps

### 1. Create the Service Account

First, we'll create a Service Account named `admin-user` in the `kubernetes-dashboard` namespace.

- **File**: `admin-user-serviceaccount.yaml`

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
```

Apply the configuration:

```shell
kubectl apply -f admin-user-serviceaccount.yaml
```

### 2. Grant Admin Permissions

Next, we associate the Service Account with the `cluster-admin` role using a ClusterRoleBinding.

- **File**: `admin-user-clusterrolebinding.yaml`

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
```

Apply the configuration:

```shell
kubectl apply -f admin-user-clusterrolebinding.yaml
```

### 3. (Optional) Create a Long-lived Token

For a long-lived token, create a Secret bound to the Service Account.

- **File**: `admin-user-secret.yaml`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
  annotations:
    kubernetes.io/service-account.name: "admin-user"
type: kubernetes.io/service-account-token
```

Apply the configuration:

```shell
kubectl apply -f admin-user-secret.yaml
```

### 4. Retrieve the Token

#### For a Short-lived Token

```shell
kubectl -n kubernetes-dashboard create token admin-user
```

#### For a Long-lived Token (if Secret was created)

```shell
kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath="{.data.token}" | base64 --decode
```


#### SSH from PC to Server
To access the Kubernetes dashboard running on your server (10.16.150.139) at port 8001 from your local PC, you can use SSH port forwarding.

```shell
ssh -L 8001:localhost:8001 [your_username]@10.16.150.139
```


### 5. Access the Dashboard

After you have retrieved the token, you can access the Kubernetes Dashboard using the following steps:

1. **Navigate to the Dashboard URL**: Open your web browser and go to the Kubernetes Dashboard URL. If you are running the Dashboard locally or through a proxy, use the following link:

   ```
   http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
   ```

2. **Login Method**: On the login screen of the Dashboard, select the **Token** login method.

3. **Enter the Token**: Paste the token you retrieved in the previous steps into the **Enter token** field on the Dashboard login page.

4. **Sign In**: Click the **Sign in** button to access the Dashboard.

By following these steps, you will be logged in as an admin user and able to interact with the Kubernetes Dashboard, viewing and managing resources in your cluster.

Remember, it's crucial to ensure your Kubernetes cluster is securely configured, especially when exposing services like the Kubernetes Dashboard. Always use secure connections (HTTPS) and consider additional security measures such as access controls and network policies to protect your cluster.

## Clean Up

To remove the created resources and revoke access:

```shell
kubectl -n kubernetes-dashboard delete serviceaccount admin-user
kubectl delete clusterrolebinding admin-user
kubectl -n kubernetes-dashboard delete secret admin-user  # If created
```


## Security Considerations

- Granting admin permissions can pose security risks. Ensure you understand the implications before proceeding.
- Regularly review your cluster's access policies and roles for best security practices.

For more details on Kubernetes Service Accounts and RBAC, refer to the official [Kubernetes documentation](https://kubernetes.io/docs/).

---

**Note:** This guide assumes basic knowledge of Kubernetes resource management using `kubectl`. Adjustments may be necessary based on your specific cluster configuration and Kubernetes version.