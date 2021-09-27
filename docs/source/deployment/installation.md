# Installation

## Clone

`git clone https://github.com/abims-sbr/GGA_Cloud.git`

## Dependencies installation

```
ansible-galaxy install -r requirements.yml
```
or to install both separately :
```
ansible-galaxy install role -r requirements.yml
ansible-galaxy install collection -r requirements.yml
```

Need to add `collections_paths = ./collections` in ansible.cfg to use collections.
