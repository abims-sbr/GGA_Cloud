GGA cloud Terraform role
========================

The terraform role creates a "terraform" folder, in the playbook directory, containing the configuration files describing the virtual machine to be deployed.

The configuration files created are:

* a providers.tf file describing the cloud provider.
* a resource.tf file describing the virtual machine to be deployed.
* a var.tf file gathering the different variables used.
* a outputs.tf file describing the hosts and ssh_cfg files to generate.

Finally, the role runs terraform to deploy the described virtual machine in the cloud.

** The role also create a new host file in the "terraform" folder (by default). Don't forget to change your host file before running next roles. **


Requirements
------------

This role is performed locally (on your local host) and need an Openstack account to be executed.


Role variables
--------------

Not all variables are listed or explained in detail. For additional information about less commonly used variables, see the defaults file.

Check also the github repository at https://github.com/abims-sbr/GGA_Cloud/tree/master/roles/abims-sbr.gga_terraform

All terraform variables should be configure either in a group_vars/localhost/terraform.yml file or at least in your playbook.


Required variables
^^^^^^^^^^^^^^^^^^

Cloud configurations variables :

* **os_auth_url**: The Identity authentication URL.
* **os_hostname**: 
* **os_project_id**: The ID of the Tenant (v2) or Project (v3).
* **os_project_name**: The Name of the Tenant (v2) or Project (v3).
* **os_user_domain_name**: The domain name where the user is located.
* **os_project_domain_id**: The domain ID where the project is located.
* **os_user_name**: The Username to login with.
* **os_network**: The name of the network.
* **terraform_password**: The Password to login with

Virtual Machine variables :

* **vm_image_name**: The name of the desired image for the resource. (Required if vm_image_id is empty).
* **vm_image_id**: The image ID of the desired image for the resource. (Required if vm_image_name is empty).
* **vm_flavor_name**: The name of the desired flavor for the resource.
* **vm_key_pair**: The name of a key pair to put on the resource. The key pair must already be created and associated with the tenant's (v2) or project's (v3) account.
* **vm_security_group**: An array of one or more security group names to associate with the server.


Optional variables
^^^^^^^^^^^^^^^^^^

You can also :

* Create and attach a volume to the instance

	* **vol_name**: A unique volume name.
	* **vol_size**: The size of the volume to create (in gigabytes).
	* **vol_type**: The type of volume to create.

* Or attach an existing volume

	* **vol_name**: A unique volume name.
	* **vol_id**: An existing volume id.


Openstack variables help
^^^^^^^^^^^^^^^^^^^^^^^^

Most of the variables are accessible at "Project tab > API Access > View Credentials" :

- os_username
- os_project_name
- os_project_id
- os_auh_url

They are also available in the Openstack RC file in "Your account > Openstack RC file". This downloads a .sh file where the previous variables are described as well as :

- os_user_domain_name
- os_project_domain_id

The `os_hostname` variable is your cloud hostname. 

The `os_network` variable is accessible in "Project tab > Network > Networks"

Instance variables are accessible at :

- vm_image_name in "Project tab > Compute > Images"
- vm_image_id in "Project tab > Compute > Images"
- vm_flavor_name in "Project tab > Compute > Instances > Launch Instance > Flavor"
- vm_key_pair in "Project tab > Compute > Key Pairs"
- vm_security_group in "Project tab > Network > Security Groups"


Usage
-----

Dry mode
^^^^^^^^

.. code-block:: bash

  ansible-playbook playbook_gga_terraform.yml --check


Real mode
^^^^^^^^^

.. code-block:: bash

  ansible-playbook playbook_gga_terraform.yml