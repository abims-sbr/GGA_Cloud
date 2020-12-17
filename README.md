# ansible

## Inventaire

`development/hosts`

## Usage

### Installer les dépendances
```
ansible-galaxy install -r requirements.yml 
```

### Lancer le playbook
#### Dry mode
```
ansible-playbook playbook_gga_genocloud.yml --check
```

#### Real mode
```
ansible-playbook playbook_gga_genocloud.yml
```

