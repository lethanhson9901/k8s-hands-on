# Prerequisities for install CSI (in this case is Rook/Ceph) on CentOS

#### Introduction
Deploying a High-Availability Kubernetes cluster requires meticulous system preparation, especially when integrating advanced storage solutions like Rook/Ceph. This guide provides detailed instructions for adjusting your system's partitions and fulfilling the prerequisites for setting up Kubernetes HA on a CentOS system.

#### Partition Adjustments for System Preparation

Properly configuring your system's partitions is crucial for optimal performance and reliability.

**Resizing a Partition from 400GB to 200GB**

1. **Delete the Incorrect Partition**:
   - Launch `fdisk` on the target disk by executing `fdisk /dev/sda`.
   - Use the `d` option to delete a partition. When prompted, enter the number of the partition you wish to delete.

2. **Create the New Partition**:
   - Still within `fdisk`, press `n` to create a new partition and choose `p` for primary.
   - When prompted for the partition number, select the same number as the deleted partition.
   - For the first sector, accept the default. For the last sector, input `+200G` to create a 200GB partition.

3. **Write Changes and Exit**:
   - Save the changes and exit `fdisk` by typing `w`.

**Converting a Partition to Raw**

1. **Unmount the Partition** (if necessary):
   - If the partition is mounted, unmount it with `umount /dev/sda3`.

2. **Remove the File System**:
   - Use `wipefs -a /dev/sda3` to erase all filesystem signatures, effectively converting the partition to a raw state.

3. **Verify the Partition is Raw**:
   - Confirm the raw status with `lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT`, ensuring the `FSTYPE` for the partition is empty.

**Re-reading the Partition Table**

- To make the system aware of the new partition table without rebooting, use:
  - `partprobe` or
  - `kpartx -av /dev/sda`.

#### Kubernetes HA Setup Prerequisites

Preparing your system for Kubernetes HA involves several crucial steps, outlined below.

1. **iSCSI Initiator Setup**:
   - Verify if the iSCSI initiator is installed with `systemctl status iscsid`.
   - If not, install it via `yum install -y iscsi-initiator-utils` and enable it with `sudo systemctl enable --now iscsid`.

2. **Verify CPU Architecture and SSE4.2 Support**:
   - Ensure SSE4.2 support with `grep -Eo 'sse4_2' /proc/cpuinfo | uniq`.

3. **Check and Upgrade Linux Kernel Version**:
   - Verify your kernel version with `uname -r`. For compatibility, ensure it's version `5.13` or higher. If not, upgrade following [VinaHost's guide](https://blog.vinahost.vn/huong-dan-upgrade-kernel-tren-centos-7/).

4. **Verify Kernel Modules**:
   - Check for the presence of necessary modules (`nvme_tcp`, `ext4`, `xfs`) with `lsmod`. Load any missing modules with `sudo modprobe {module_name}`.

5. **Install Helm (v3.7 or later)**:
   - Follow the provided script commands to install Helm, ensuring you have the latest version for Kubernetes management.

6. **Verify Available Resources (CPU cores and RAM)**:
   - Check the number of CPU cores with `nproc` and the total RAM with `free -h`. Also, verify the allocation of HugePages needed for certain workloads.

7. **Networking Requirements**:
   - Confirm that necessary ports are not in use and are not blocked by the firewall, adjusting settings with `iptables` as necessary.

#### Troubleshooting Tips

- Maintain a backup or recovery plan, especially when performing sensitive operations like kernel upgrades or filesystem modifications.
- For kernel or module-related issues, ensure compatibility with your current CentOS version and the target kernel version.




# Rook Quickstart Guide

## Introduction

Rook turns distributed storage systems into self-managing, self-scaling, self-healing storage services. It automates the tasks of a storage administrator: deployment, bootstrapping, configuration, provisioning, scaling, upgrading, migration, disaster recovery, monitoring, and resource management.

## Prerequisites

Before you begin, ensure your system meets the following requirements:

- A Kubernetes cluster running version 1.13 or later
- `kubectl` installed and configured to connect to your Kubernetes cluster
- Knowledge of Kubernetes concepts and basic operations

## Installation

### Step 1: Clone the Rook Repository

```bash
git clone --single-branch --branch master https://github.com/rook/rook.git
cd rook/cluster/examples/kubernetes/ceph
```

### Step 2: Deploy the Rook Operator

Deploy the Rook operator to manage Ceph storage within your Kubernetes cluster.

```bash
kubectl create -f crds.yaml -f common.yaml -f operator.yaml
```

### Step 3: Create a Rook Ceph Cluster

After the operator is up and running, create a Rook Ceph cluster.

```bash
kubectl create -f cluster.yaml
```

### Step 4: Create Storage Class

Define storage classes to define how storage can be consumed.

```bash
kubectl create -f csi/rbd/storageclass.yaml
```

## Verify the Installation

Ensure all pods in the `rook-ceph` namespace are in the `READY` state.

```bash
kubectl -n rook-ceph get pod
```

## Basic Usage

- **Creating a Block Storage**: To dynamically provision storage for your applications, use the storage class created earlier.

- **File System**: Deploy the Ceph filesystem by running `kubectl create -f filesystem.yaml`.

- **Object Storage**: Start the Rook Ceph Object Gateway to provide S3-compatible storage by executing `kubectl create -f object.yaml`.

## Advanced Configuration

- **Customizing Cluster Settings**: Customize your cluster settings using the CephCluster CRD.
- **Upgrading Rook**: Follow the upgrade guide to safely upgrade Rook and Ceph versions.

## Troubleshooting

- Check operator logs: `kubectl -n rook-ceph logs deployment/rook-ceph-operator`
- Ensure all nodes have the necessary prerequisites.
- Review the Rook [Troubleshooting Guide](https://rook.io/docs/rook/latest/ceph/troubleshooting.html).

## Additional Resources

- [Rook Website](https://rook.io/)
- [Rook GitHub Repository](https://github.com/rook/rook)
- [Rook Documentation](https://rook.io/docs/rook/latest/)
