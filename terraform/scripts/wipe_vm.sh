if [ "$#" = 1 ]; then
	terraform apply -replace "libvirt_domain.decalvm[\"$1\"]" -replace "libvirt_volume.decalvm_volume[\"$1\"]"
else
	echo "Usage: wipe_vm.sh <ocfusername>"
fi
