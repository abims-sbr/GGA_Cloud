GGA cloud Terraform role
========================

The terraform role creates a "terraform" folder near to the playbook containing the configuration files of the virtual machine to be deployed.

The configuration files created are:

* a providers.tf file describing the cloud provider.
* a resource.tf file describing the virtual machine to deploy.
* a var.tf file gathering the different variables used.
* an outputs.tf file describing the hosts and ssh_cfg files to generate.

Finally, the role runs terraform to deploy the described virtual machine in the cloud.
