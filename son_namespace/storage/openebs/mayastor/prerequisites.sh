#!/bin/bash

# Upgrade Linux Kernel
echo "Upgrading Linux Kernel to version 5.15.4"
yum install xz -y
wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.15.4.tar.xz
tar -Jxvf linux-5.15.4.tar.xz
cd linux-5.15.4

# Install development tools and dependencies
echo "Installing development tools and required dependencies"
yum groupinstall "Development Tools" -y
yum install gcc -y
yum install ncurses ncurses-devel -y
yum install openssl-devel bc flex bison -y
yum install libssl-dev bc libelf-dev elfutils-libelf-devel -y
yum install centos-release-scl -y
yum install devtoolset-7 -y
scl enable devtoolset-7 bash

# Prepare and build the kernel source
echo "Preparing and building the kernel source"
make mrproper
make menuconfig
make
make modules
make modules_install
make install

# Update GRUB configuration
echo "Updating GRUB configuration"
menuentry=$(awk -F\' '$1=="menuentry " {print $2}' /etc/grub2.cfg)
echo "Menu Entry Identified: $menuentry"
grub2-set-default "CentOS Linux (5.15.4) 7 (Core)"
if [ -d /sys/firmware/efi ]; then
    echo "UEFI mode detected"
    grub2-mkconfig -o /boot/efi/EFI/centos/grub.cfg
else
    echo "BIOS (Legacy) mode detected"
    grub2-mkconfig -o /boot/grub2/grub.cfg
fi

# Install Helm 3
echo "Installing Helm 3"
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh

# Configure HugePages
echo "Configuring HugePages"
echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
echo vm.nr_hugepages = 1024 | sudo tee -a /etc/sysctl.conf
echo "HugePages Configuration:"
grep HugePages_Total /proc/meminfo
grep Hugepagesize /proc/meminfo

sudo modprobe nvme-tcp
sudo modprobe ext4
sudo modprobe xfs


# Reboot the system
echo "Rebooting system to apply all changes..."
reboot
