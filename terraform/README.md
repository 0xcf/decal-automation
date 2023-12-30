# Decal VMs Terraform Infrastructure

## Common Commands
Display the plan of changes that will be taken:
```sh
terraform plan
```

Apply the proposed changes to the infrastructure:
```sh
terraform apply
```

Recreate the VM for user waddles:
```sh
./scripts/wipe_vm.sh waddles
```

Reset the VM password for user waddles:
```sh
./scripts/reset_password.sh waddles
```

## Getting Started
Make sure to create a `terraform.tfvars` file using the `terraform.tfvars.example` provided.
You'll need to be root to run terraform and make sure your ssh key is added to the root user on implosion (edit `~root/.ssh/authorized_keys` on implosion).

Get (or generate) a root SSH key for the VMs and place it in `../data/decal_root` and `../data/decal_root.pub`. This will allow you to access all student VMs in case a password reset or interactive debugging is required.

Create `../data/students.in.csv` which contains the OCF username and email for each student to create a VM for:
```csv
username,email
waddles,waddles@ocf.berkeley.edu
```

You can then use that to create `../data/students.csv`, which defines the VMs that terraform will provision:
```sh
python3 ../transform_students_csv.py
```

Run the following command to ensure everything is okay:
```sh
terraform plan
```

Then hit the apply:
```sh
terraform apply
```
If you get an error about not finding a cloud-init iso, this is because of a bug in the libvirt provider. Just run `terraform apply` again and it'll figure itself out. (https://github.com/dmacvicar/terraform-provider-libvirt/issues/973)

Once all the VMs have been created, you can send the students their login information:
```sh
python3 ../send_vms.py
```

## Other Commands

To reboot all VMs:
```sh
python3 ./scripts/reboot_all.py
```

To reboot a VM:
```sh
./scripts/reboot.sh <ocfusername>
```

To wipe a VM:
```sh
./scripts/wipe_vm.sh <ocfusername>
```

## Other Information

If you need to destroy all VMs at the end of the semester, just clear out the entire `../data/students.csv` except for the header line and run `terraform apply`.

If you migrate the location of the storage pool, make sure it's added to apparmor in `/etc/apparmor.d/local/abstractions/libvirt-qemu` otherwise you'll get permissions errors.
