output "vms" {
  value = "${digitalocean_droplet.decal_vms.*}"
}
