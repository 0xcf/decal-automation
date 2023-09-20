#!/bin/bash
set -euo pipefail

if [ "$#" = 1 ]; then
	username=$1
	terraform apply -replace "libvirt_domain.decalvm[\"$username\"]" -replace "libvirt_volume.decalvm_volume[\"$username\"]"
else
	echo "Usage: $0 <ocfusername>"
fi
