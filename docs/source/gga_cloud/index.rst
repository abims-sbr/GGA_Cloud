GGA cloud ansible roles
=======================

GGA cloud is a project which aims to automate the deployment of the GGA environment in a cloud infrastructure.

It uses the open-source tool Ansible for software provisioning, configuration management and application deployment.

3 Ansible roles have been developped :

- gga_terraform : To deploy a virtual machine in a cloud infrastructure (currently using Openstack technology).

- gga_install : To deploy Galaxy Genome Annotation docker stacks.

- gga_load_data : To import data into the docker Galaxy history.


.. toctree::
   :maxdepth: 2

   gga_terraform
   gga_install
   gga_load_data