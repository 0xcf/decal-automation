variable "do_token" {}
variable "dnsimple_token" {}
variable "dnsimple_account" {}

provider "digitalocean" {
  token = "${var.do_token}"
}

provider "dnsimple" {
  token = "${var.dnsimple_token}"
  account = "${var.dnsimple_account}"
}
