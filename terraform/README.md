Make sure to create a `terraform.tfvars` file using the `terraform.tfvars.example` provided.
You'll need to be root to run terraform and make sure your ssh key is added to the root user on implosion.

Get (or generate) a root SSH key and place it in `../data/decal_root` and `../data/decal_root.pub`.

Run the following command to ensure everything is okay:

```sh
terraform plan
```

Then hit the apply:

```sh
terraform apply
```

To recreate the VM for user waddles:
```sh
terraform apply -replace libvirt_domain.decalvm[\"waddles\"] -replace libvirt_volume.decalvm_volume[\"waddles\"]
```

If you migrate the location of the storage pool, make sure it's added to apparmor in `/etc/apparmor.d/local/abstractions/libvirt-qemu` otherwise you'll get permissions errors.

To reboot a VM:
```sh
./scripts/reboot.sh <ocfusername>
```

To reset a user's VM password:
```sh
./scripts/reset_password.sh <ocfusername>
```

To wipe a VM:
```sh
./scripts/wipe_vm.sh <ocfusername>
```
