Galaxy Genome Annotation Cloud installation & usage
===================================================


Requirements
------------

For the use of Ansible, Python 3 (versions 3.5 and higher) is required. Roles were developped under Ansible-core (>= 2.11) & Ansible (>= 4.0.0).

Git is also required to clone the [GGA cloud](https://github.com/abims-sbr/GGA_Cloud.git) github repository.


Installation
------------

Clone repository from github
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`git clone https://github.com/abims-sbr/GGA_Cloud.git`

Ansible roles requirements installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

```
ansible-galaxy install -r requirements.yml
```

or to install both separately :

```
ansible-galaxy install role -r requirements.yml

ansible-galaxy install collection -r requirements.yml
```

Need to add `collections_paths = ./collections` in ansible.cfg to use collections.


Usage
-----

Dry mode
^^^^^^^^

```
ansible-playbook terraform.yml --check

ansible-playbook gga_install.yml --check

ansible-playbook gga_load_data.yml --check
```

Real mode
^^^^^^^^^

```
ansible-playbook terraform.yml
ansible-playbook gga_install.yml
ansible-playbook gga_load_data.yml
```
