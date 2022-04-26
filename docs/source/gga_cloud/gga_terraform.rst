GGA cloud Terraform role
========================

The terraform role creates a "terraform" folder, in the playbook directory, containing the configuration files describing the virtual machine to be deployed. 
It also creates the "hosts" and "ssh.cfg" files that allow you to connect to the virtual machine deployed in order to run the following playbooks.

Role steps :

* Create a terraform folder in the playbook directory

* Create the following files into the terraform folder

	* a providers.tf file describing the cloud provider.
	* a resource.tf file describing the virtual machine to be deployed.
	* a var.tf file gathering the different variables used.
	* a outputs.tf file describing the hosts and ssh_cfg files to generate.
	* an ansible inventory file called hosts
	* a ssh.cfg file setting up the SSH bastion

* Run terraform to deploy the described virtual machine in the cloud.

* Copy the hosts and ssh.cfg file in the correct directory and create their backup files.


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
* **os_hostname**: The cloud hostname.
* **os_project_id**: The ID of the Tenant (v2) or Project (v3).
* **os_project_name**: The Name of the Tenant (v2) or Project (v3).
* **os_user_domain_name**: The domain name where the user is located.
* **os_project_domain_id**: The domain ID where the project is located.
* **os_user_name**: The Username to login with.
* **os_password**: The Password used to log in to your cloud account.
* **os_network**: The name of the network.

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


Troubleshooting
---------------

After running this playbook. You may have to run the following command into the virtual machine to update some librairies :

.. code-block:: bash

  apt-get update -y --allow-releaseinfo-change
  apt-get upgrade -y

------

In case of using a storage volume, you must currently also mount it. If this is the first time using this volume, you need to create a file system on it. To check if there is already one, using this command:

.. code-block:: bash

  lsblk -f

If there are none, you need to create it:

.. code-block:: bash

  mkfs.ext4 /dev/vdb

You can then mount the volume anywhere you wish.

mkdir /mnt/myfolder
mount /dev/vdb /mnt/myfolder
