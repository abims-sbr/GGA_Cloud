# Deploy an instance for GGA with TERRAFORM (currently for OpenStack CI)

This role creates a "terraform" folder containing the configuration files of the virtual machine to be deployed.

## Role tasks

- Create a terraform folder.
- Generate terraform templates for configuration files.
- Run terraform to apply configurations.

## Requirements

- Community General Collection

## Role Variables

### Global

- terraform_dir: The path where the terraform folder is created
- hosts_path: The path where the hosts file is created

### Provider

The provider's configurations can be obtained by connecting to the account of the user on which you want to install an instance, then in the "user" panel, downloading the "OpenStack RC v3 file".

- os_auth_url : The identity authentication URL
- os_project_id : The project id (tenant (v2) = project (v3))
- os_project_name : The project name
- os_user_domain_name : The domain name where the user is located
- os_project_domain_id : The project domain id
- os_user_name : The user name to login with
- os_network : The name of the network
- terraform_password : The user password to login with

### Resource

Resource configurations can be found by logging into the user account in:
"Project -> Compute -> Images" for the image name desired.
"Project -> Compute -> Instance -> Deploy instance -> Template" for the flavor list available.
"Project -> Network -> Networks" for the network name.

- vm_name : A unique instance name
- vm_image_name : The image name to installed. (Required if vm_image_id is empty).
- vm_image_id : The image ID of the desired image. (Required if vm_image_name is empty).
- vm_flavor_name : The name of the desired flavor for the resource.
- vm_key_pair : The name of a key pair to put on the resource. The key pair must already be created and associated with the tenant's (v2) or project's (v3) account.
- vm_security_group : An array of one or more security group names to associate with the server.

In case of volume to created and/or attached :
- vol_name : A unique volume name
- vol_size : The volume size to create (in gigabytes)
- vol_type : The volume type
- vol_id : An existing volume id

### Output

- os_vms_user : The user with to connect with on the VM
- ssh_key_path : The path to your local ssh public key

## Example Playbook

```
- hosts: localhost
  connection: local
  vars:
    os_auth_url: https://auth_url.com
    os_hostname: your_hostname.com
    os_project_id: projectid
    os_project_name: projectname
    os_project_domain_id: domainid
    os_user_name: username
    terraform_password: password
    vm_image_name: image_name
    vm_image_id: image_id
    vm_flavor_name: flavor
    vm_key_pair: your_key_pair
    os_network: network
  roles:
    - gga_terraform
```