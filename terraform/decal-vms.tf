variable "data_file" {}
variable "pvt_key_file" {}
variable "pub_key_file" {}
variable "ssh_fingerprint" {}


locals {
    # Import all decal student data
    data = csvdecode(file("${var.data_file}"))
}


resource "digitalocean_ssh_key" "decal_key" {
    name    = "decal-key"
    public_key = "${file("${var.pub_key_file}")}"
}

resource "digitalocean_droplet" "decal_vms" {
    depends_on = [digitalocean_ssh_key.decal_key]

    for_each = { for inst in local.data : inst.username => inst }
    image = "ubuntu-18-04-x64"
    name = "${each.value.username}.decal.xcf.sh"
    region = "sfo2"
    size = "s-1vcpu-1gb"
    private_networking = false
    ssh_keys = [
      "${var.ssh_fingerprint}"
    ]

    provisioner "file" {
        connection {
            type     = "ssh"
            user     = "root"
            private_key = "${file("${var.pvt_key_file}")}"
            host    = self.ipv4_address
        }
        source      = "sshd_config"
        destination = "/etc/ssh/sshd_config"
    }

    # Set the motd         
    provisioner "file" {
        connection {
            type     = "ssh"
            user     = "root"
            private_key = "${file("${var.pvt_key_file}")}"
            host    = self.ipv4_address
        }
        source      = "motd"
        destination = "/etc/motd"
    }

    provisioner "remote-exec" {
        connection {
            type     = "ssh"
            user     = "root"
            private_key = "${file("${var.pvt_key_file}")}"
            host    = self.ipv4_address
        }
        inline = [
        # Set the hostname to be FQDN
        "sudo hostname ${each.value.username}.decal.xcf.sh",

        # Add the user and give them root access
        "sudo useradd ${each.value.username} -s /bin/bash -m",
        "sudo echo ${each.value.username}:${each.value.password} | sudo chpasswd",
        "sudo usermod -aG sudo ${each.value.username}",
        "sudo service sshd restart",
       	"sudo passwd -e ${each.value.username}",

        # Populate the motd with data
        "sudo sed -i 's/$HOSTNAME/${each.value.username}/g' /etc/motd",
        "sudo sed -i 's/$IP/${self.ipv4_address}/g' /etc/motd",
	
        # Reboot to allow MOTD to change. This is a hack.
        "sudo shutdown -r +60"
        ]
    }
}

resource "dnsimple_record" "a-records" {
    for_each = digitalocean_droplet.decal_vms
    domain = "xcf.sh"
    name   = "${regex("(.+\\.decal)", "${each.value.name}")[0]}"
    value  = "${each.value.ipv4_address}"
    type   = "A"
}

