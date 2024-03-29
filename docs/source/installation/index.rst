Galaxy Genome Annotation Cloud installation & usage
===================================================

Requirements
------------

For the use of Ansible playbooks, Ubuntu 18.04 or higher is required.

Python 3 (versions 3.5 and higher) is required. Roles were developped under Ansible-core (>= 2.11) & Ansible (>= 4.0.0).

Git is also required to clone the `GGA cloud <https://github.com/abims-sbr/GGA_Cloud.git>`_ github repository.

The roles are currently being developed for cloud infrastructures based on Openstack technology. So you need an account on a Openstack cloud.


For smoother use of GGA, a 20GB size virtual machine with 16GB RAM is recommended.


Installation
------------

Clone repository from github
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

  git clone https://github.com/abims-sbr/GGA_Cloud.git

Ansible roles requirements installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

  ansible-galaxy install -r requirements.yml

or to install both separately :

.. code-block:: bash

  ansible-galaxy install role -r requirements.yml
  ansible-galaxy install collection -r requirements.yml


Need to add `collections_paths = ./collections` in ansible.cfg to use collections.