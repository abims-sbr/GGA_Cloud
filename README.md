# ansible

## Inventaire

`development/hosts`

## Usage

### Installer les dépendances
```
ansible-galaxy install -r requirements.yml 
```
ou pour les installer les 2 séparément :
```
ansible-galaxy install role -r requirements.yml 
ansible-galaxy install collection -r requirements.yml 
```

Besoin d'ajouter `collections_paths = ./collections` dans ansible.cfg pour utiliser les collections.

### Lancer le playbook
#### Dry mode
```
ansible-playbook playbook_gga_genocloud.yml --check
```

#### Real mode
```
ansible-playbook playbook_gga_genocloud.yml
```

