variable "data_file" {
  default = "./data_test.csv"
}

locals {
  # Import all decal student data
  data       = csvdecode(file(var.data_file))
  cloud_init = "${path.module}/cloud_init.cfg"
  decalvm_ip = {
    for student in local.data : student.username => {
      v4 = "128.32.128.${student.id}"
      v6 = "2607:f140:8801::2:${student.id}"
    }
  }
}

resource "libvirt_pool" "decalvm_pool" {
  name = "decalvm"
  type = "dir"
  path = "/mnt/decalfs"

  lifecycle {
    // make sure to not destroy pool, otherwise all VMs will lose their data
    prevent_destroy = true
  }
}

# We fetch the latest ubuntu release image from their mirrors
resource "libvirt_volume" "ubuntu_img" {
  name   = "ubuntu-2204.img"
  pool   = libvirt_pool.decalvm_pool.name
  source = "https://cloud-images.ubuntu.com/releases/jammy/release/ubuntu-22.04-server-cloudimg-amd64-disk-kvm.img"
  format = "qcow2"

  lifecycle {
    // mostly prevented because it's a pain to download it again, but not too important
    prevent_destroy = true
  }
}


resource "libvirt_cloudinit_disk" "decalvm_init" {
  for_each = { for student in local.data : student.username => student }

  name = "decalvm-init-${each.value.username}.iso"
  user_data = templatefile(local.cloud_init, {
    student = each.value,
    ip      = local.decalvm_ip[each.value.username].v6,
    fqdn    = "${each.value.username}.${trimsuffix(var.dns_zone, ".")}"
  })
  network_config = <<-EOT
  version: 2
  ethernets:
    ens3:
      addresses: [${local.decalvm_ip[each.value.username].v6}/64]
      gateway6: 2607:f140:8801::1
      nameservers:
        search: [ocf.berkeley.edu]
        addresses: [2607:f140:8801::1:52]
  EOT
  pool           = libvirt_pool.decalvm_pool.name
}

resource "libvirt_volume" "decalvm_volume" {
  for_each = { for student in local.data : student.username => student }

  name             = "decalvm-${each.value.username}.img"
  size             = 32212254720 # 30 GB in bytes
  pool             = libvirt_pool.decalvm_pool.name
  base_volume_id   = libvirt_volume.ubuntu_img.id
  base_volume_pool = libvirt_volume.ubuntu_img.pool
}

# Create the machine
resource "libvirt_domain" "decalvm" {
  for_each = { for student in local.data : student.username => student }

  name   = "decalvm-${each.value.username}"
  memory = "3072"
  vcpu   = 2

  cpu {
    mode = "host-passthrough"
  }

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
}

resource "dns_aaaa_record_set" "decalvm_aaaarecord" {
  for_each = { for student in local.data : student.username => student }

  name      = each.value.username
  addresses = [local.decalvm_ip[each.value.username].v6]
  zone      = var.dns_zone
}
