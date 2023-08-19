Make sure to create a `terraform.tfvars` file using the `terraform.tfvars.example` provided.

If running on macOS, make sure to increase your `ulimit` since Terraform will attempt to use many ssh-agent's to provision everything. I recommend `ulimit -n 4096`.

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
