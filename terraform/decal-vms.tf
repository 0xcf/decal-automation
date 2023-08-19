variable "data_file" {
  default = "./data_test.csv"
}

locals {
  # Import all decal student data
  data        = csvdecode(file(var.data_file))
  cloud_init  = file("${path.module}/cloud_init.cfg")
  ipv4_prefix = "128.32.128"
  ipv6_prefix = "2607:f140:8801::2"
}

# We fetch the latest ubuntu release image from their mirrors
resource "libvirt_volume" "ubuntu_img" {
  name   = "ubuntu-2204.img"
  pool   = "images"
  source = "https://cloud-images.ubuntu.com/releases/jammy/release/ubuntu-22.04-server-cloudimg-amd64-disk-kvm.img"
  format = "qcow2"
}


resource "libvirt_cloudinit_disk" "decalvm_init" {
  for_each = { for student in local.data : student.username => student }

  name           = "decalvm-init-${each.value.username}.iso"
  user_data      = local.cloud_init
  network_config = <<-EOT
  version: 2
  ethernets:
    ens3:
      addresses: [${local.ipv4_prefix}.${each.value.id}/24, ${local.ipv6_prefix}:${each.value.id}/64]
      gateway4: 169.229.226.1
      gateway6: 2607:f140:8801::1
      nameservers:
        search: [ocf.berkeley.edu]
        addresses: [169.229.226.22, 2607:f140:8801::1:22]
  EOT
  pool           = "images"
}

resource "libvirt_volume" "decalvm_volume" {
  for_each = { for student in local.data : student.username => student }

  name             = "decalvm-${each.value.username}.img"
  size             = 4000000000 # 4 GB in bytes
  pool             = "images"
  base_volume_id   = libvirt_volume.ubuntu_img.id
  base_volume_pool = libvirt_volume.ubuntu_img.pool
}

# Create the machine
resource "libvirt_domain" "decalvm" {
  for_each = { for student in local.data : student.username => student }

  name   = "decalvm-${each.value.username}"
  memory = "2048"
  vcpu   = 2

  cloudinit = libvirt_cloudinit_disk.decalvm_init[each.value.username].id

  network_interface {
    bridge = "br0"
  }

  # IMPORTANT: this is a known bug on cloud images, since they expect a console
  # we need to pass it
  # https://bugs.launchpad.net/cloud-images/+bug/1573095
  console {
    type        = "pty"
    target_port = "0"
    target_type = "serial"
  }

  console {
    type        = "pty"
    target_port = "1"
    target_type = "virtio"
  }

  disk {
    volume_id = libvirt_volume.decalvm_volume[each.value.username].id
  }

  provisioner "remote-exec" {
    connection {
      type        = "ssh"
      user        = "root"
      private_key = file("~/.ssh/id_ed25519")
      host        = "${local.ipv6_prefix}:${each.value.id}"
    }
    inline = [
      # Set the hostname to be FQDN
      "hostnamectl set-hostname ${each.value.username}.decal.xcf.sh",

      # Add the user and give them root access
      "useradd ${each.value.username} -s /bin/bash -m",
      "echo ${each.value.username}:${each.value.password} | chpasswd",
      "usermod -aG sudo ${each.value.username}",
      "printf '${each.value.username} ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/decal",
      "service sshd restart",
      # Expire password so user is forced to change on first login
      "passwd -e ${each.value.username}",

      # Populate the motd with data
      "sed -i 's/$HOSTNAME/${each.value.username}/g' /etc/motd",
      "sed -i 's/$IP/${local.ipv4_prefix}.${each.value.id}/g' /etc/motd",

      # Remove motd spam
      "apt purge --yes ubuntu-advantage-tools",
    ]
  }
}

resource "dnsimple_zone_record" "decalvm_arecord" {
  for_each = { for student in local.data : student.username => student }

  name      = "${each.value.username}.decal"
  type      = "A"
  value     = "${local.ipv4_prefix}.${each.value.id}"
  zone_name = "xcf.sh"
}

resource "dnsimple_zone_record" "decalvm_aaaarecord" {
  for_each = { for student in local.data : student.username => student }

  name      = "${each.value.username}.decal"
  type      = "AAAA"
  value     = "${local.ipv6_prefix}:${each.value.id}"
  zone_name = "xcf.sh"
}
