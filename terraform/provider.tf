terraform {
  required_providers {
    libvirt = {
      source  = "dmacvicar/libvirt"
      version = "~>0.7.1"
    }
    dnsimple = {
      source  = "dnsimple/dnsimple"
      version = "~>1.1.2"
    }
  }
}

variable "libvirt_uri" {
  sensitive = true
  default   = "qemu:///system"
}

variable "dnsimple_account" {
  sensitive = true
}
variable "dnsimple_token" {
  sensitive = true
}

provider "libvirt" {
  uri = var.libvirt_uri
}

provider "dnsimple" {
  account = var.dnsimple_account
  token   = var.dnsimple_token
}
