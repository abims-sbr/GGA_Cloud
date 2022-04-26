.. image:: https://img.shields.io/readthedocs/gga-cloud   
   :target: https://gga-cloud.readthedocs.io/en/latest/index.html
   :alt: Read the Docs

About the project
=================

The Galaxy Genome Annotation (GGA) (https://galaxy-genome-annotation.github.io) project consists of several projects and tool suites that are working closely together to deliver a comprehensive, scalable and easy to use Genome Annotation experience. The Galaxy Genome annotation environment not only offers a wide array of high-profile tools in Galaxy for structural and functional annotation, but also a highly integrated set of “dockerized” GMOD tools, a collection of open-source applications for visualizing, annotating, and managing genomic data (JBrowse, Apollo, Tripal, Chado). Galaxy is used as a data loading orchestrator for administrators, with dedicated Galaxy tools and workflows to interact with GMOD tools, and Python libraries to make all tools work together.

The EOSC-Life project aims to create an open collaborative digital space for life science in the European Open Science Cloud (EOSC). As part of the EOSC-Life WP2, dedicated to make computational tools, workflows and registries FAIR, we planned to provide the GGA environment available in the cloud. So we are currently developing Ansible recipes deploy the GGA environment in an Openstack cloud infrastructure. These Ansible recipes allow the deployment of a Virtual Machine in a cloud via the Terraform software, the installation of the GGA environment and its dependencies, as well as loading data into the Galaxy library.


Ansible
=======

Inventory
---------

`development/hosts`


Roles
-----

gga_terraform
^^^^^^^^^^^^^

The terraform role creates a "terraform" folder near to the playbook containing the configuration files of the virtual machine to be deployed.

The configuration files created are:

- a providers.tf file describing the cloud provider.
- a resource.tf file describing the virtual machine to deploy.
- a var.tf file gathering the different variables used.
- an outputs.tf file describing the hosts and ssh_cfg files to generate.

Finally, the role runs terraform to deploy the described virtual machine in the cloud.

gga_install
^^^^^^^^^^^

The gga_install role create directory tree for organisms and deploy stacks for the input organisms as well as Traefik stacks.

The gga_install role :

- installs python requirements.
- clones the [gga_load_data](http://gitlab.sb-roscoff.fr/abims/e-infra/gga_load_data/tree/master) repository and install some python librairies required by GGA.
- generates a config.yml and input.yml required by gga_load_data scripts and runs gga_init.py scripts that deploy GGA docker stacks.

gga_load_data
^^^^^^^^^^^^^

The gga_load_data role, first, generates the directory tree into the organism src_data subfolders and then copies data files into the src_data directory tree.

In a second time, the role creates a “Project Data” library in the Galaxy instance, mirroring the “src_data” folder of the current organism directory tree.

Usage
-----

Dependencies installation
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

  ansible-galaxy install -r requirements.yml 

or to install both separately :

.. code-block:: bash

  ansible-galaxy install role -r requirements.yml 
  ansible-galaxy install collection -r requirements.yml 

Need to add `collections_paths = ./collections` in ansible.cfg to use collections.

Run playbooks
^^^^^^^^^^^^^

**Dry mode**

.. code-block:: bash

  ansible-playbook terraform.yml --check
  ansible-playbook gga_install.yml --check
  ansible-playbook gga_load_data.yml --check

**Real mode**

.. code-block:: bash

  ansible-playbook terraform.yml
  ansible-playbook gga_install.yml
  ansible-playbook gga_load_data.yml

.. figure:: https://github.com/abims-sbr/GGA_Cloud/blob/master/static/images/gga_cloud.png

   *Cuboids represent Docker containers. Hexagon represent a set of Docker container for a species. Black arrows represent HTTP traffic. Blue arrows represent data exchange performed using Galaxy tools. White arrows represent data exchange inherent in applications. Grey arrows represent data/workflow import using Galaxy API.*

.. image:: https://github.com/abims-sbr/GGA_Cloud/blob/master/static/images/eosclogo.png
   :align: left

This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 824087.

.. image:: https://github.com/abims-sbr/GGA_Cloud/blob/master/static/images/eu_flag.jpg
   :align: right