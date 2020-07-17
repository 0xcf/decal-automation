Make sure to create a `terraform.tfvars` file using the `terraform_example.tfvars` provided.

If running on macOS, make sure to increase your `ulimit` since Terraform will attempt to use many ssh-agent's to provision everything. I recommend `ulimit -n 4096`.

Run the following command to ensure everything is okay:

```
terraform plan
```

Then hit the apply:

```
terraform apply
```