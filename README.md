# Ansible

![cloud_scheme](https://github.com/abims-sbr/GGA_Cloud/blob/master/static/images/cloud_scheme.png)

## Inventory

`development/hosts`

## Use

### Dependencies installation
```
ansible-galaxy install -r requirements.yml 
```
or to install both separately :
```
ansible-galaxy install role -r requirements.yml 
ansible-galaxy install collection -r requirements.yml 
```

Need to add `collections_paths = ./collections` in ansible.cfg to use collections.

### Run playbooks
#### Dry mode
```
ansible-playbook playbook_terraform.yml --check
ansible-playbook playbook_gga_genocloud.yml --check
```

#### Real mode
```
ansible-playbook playbook_terraform.yml
ansible-playbook playbook_gga_genocloud.yml
```
