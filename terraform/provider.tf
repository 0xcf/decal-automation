terraform {
  required_providers {
    libvirt = {
      source  = "dmacvicar/libvirt"
      version = "~>0.7.6"
    }
    dns = {
      source  = "hashicorp/dns"
      version = "~>3.4.0"
    }
  }
}

variable "libvirt_uri" {
  description = "Connection string to access libvirt hypervisor"
  type        = string
  sensitive   = true
  default     = "qemu:///system"
}

variable "dns_server" {
  description = "Address of DNS server"
  type        = string
  default     = "ns.ocf.berkeley.edu"
}
variable "dns_zone" {
  description = "DNS zone name (fully-qualified)"
  type        = string
  default     = "decal.ocf.io."
}
variable "dns_key_secret" {
  description = "Update key for DNS zone"
  type        = string
  sensitive   = true
}

provider "libvirt" {
  uri = var.libvirt_uri
}

provider "dns" {
  update {
    server        = var.dns_server
    key_name      = var.dns_zone
    key_algorithm = "hmac-sha512"
    key_secret    = var.dns_key_secret
  }
}
