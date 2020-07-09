# TERRAFORM

https://www.jesuisundev.com/comprendre-terraform-en-5-minutes/

Tutoriel :
https://learn.hashicorp.com/terraform/getting-started/install


## C'EST QUOI ?

Terraform est un outil qui permet de déclarer, via notre code, ce que l'on veut pour notre infrastructure. 
Dans des fichiers de configuration structurés on va pouvoir manager automatiquement notre infrastructure sans action manuelle, que ça soit l’approvisionnement initial, la mise à jour ou la destruction de l'infrastructure.

Terraform opte pour la façon de faire dite déclarative. On déclare dans les fichiers de configs l’état désiré de l'infrastructure. Terraform ne va faire qu’exécuter le minimum pour arriver à l’état désiré.


## COMMENT CA MARCHE ?

Terraform opte pour l’approche dite “push”. Il va prendre l’état déclaré dans les fichiers de configuration et pousser les modifications vers le provider de destination.

Terraform n’est pas limité à un provider (Amazon WS) ou au Cloud de façon générale. Presque tous les types d’infrastructure peuvent être représentés comme une ressource dans Terraform. Des containers docker sur une machine en local à un compte cloud sur DigitalOcean.


### BLOCS

- provider.tf

Le bloc provider configure le provider nommé, dans notre cas openstack, qui est responsable de la création et du management des ressources.

https://www.terraform.io/docs/providers/index.html

- resource.tf

Le bloc ressource défini une partie de l'infrastructure. Une ressource peut être un composant physique ou une ressource logique.

https://www.terraform.io/docs/configuration/resources.html

- variables.tf

La bloc variable défini l'ensemble des variables utilisées. Il est divisé en 2 types :

1. Inputs

Les inputs sont utilisés pour définir des valeurs qui configurent l'infrastructure. Ces valeurs peuvent être utilisées à plusieurs reprises sans avoir à se souvenir de chacune de leurs occurrences au cas où elles auraient besoin d'être mises à jour.

2. Outputs

Les outputs, en revanche, sont utilisés pour obtenir des informations sur l'infrastructure après le déploiement. Celles-ci peuvent être utiles pour transmettre des informations telles que les adresses IP pour la connexion au serveur.

https://upcloud.com/community/tutorials/terraform-variables/


## INSTALLATION (Linux)

- Télécharger le package approprié : https://www.terraform.io/downloads.html

	`wget https://releases.hashicorp.com/terraform/0.12.28/terraform_0.12.28_linux_amd64.zip`

- Dézipper le package

	`unzip terraform_0.12.24_linux_amd64.zip`

- Déplacer le binaire dans le PATH

	`mv terraform /usr/local/bin`


## CONFIGURATIONS

La majorité des configurations sont récupérables sur le cloud Genouest dans ce cas ci. 

### Provider

Les configurations du provider peuvent être obtenues en se connectant au compte de l'utilisateur sur lequel on souhaite installer une instance, puis dans le panneau "user" dans le coin supérieur droit, en téléchargeant le "Fichier OpenStack RC v3".

- auth_url : URL d'authentification
- tenant_id : Identifiant du projet (tenant (v2) = projet (v3))
- tenant_name : Nom du projet
- user_domain_name : Le nom du domaine dans lequel l'utilisateur se trouve
- project_domain_id : L'identifiant du domaine dans lequel le projet se trouve
- user_name : Le nom de l'utilisateur avec lequel se connecter
- password : Le mot de passe de l'utilisateur avec lequel se connecter


### Resource

Les configurations des ressources se trouve en se connectant au compte utilisateur dans : 
"Projet -> Compute -> Images" pour le nom de l'image souhaitée
"Projet -> Compute -> Instance -> Lancer une instance -> Gabarit" pour la liste des gabarits disponible
"Projet -> Réseau -> Réseaux" pour le nom du réseau.

- name : Nom de l'instance
- image_name : Nom de l'image à installer
- flavor_name : Nom du gabarit 
- network { name } : Nom du réseau


## COMMANDES

- Initialisation d'un working directory terraform

	`terraform init`
	
- Validation des fichiers de configuration

	`terraform validate`

- Génère et affiche le plan d'éxecution

	`terraform plan`
	
- Application des changements sur l'infrastructure

	`terraform apply`
	
- Inspection du status de l'infrastructure

	`terraform show`
	
- Suppression de l'infrastructure

	`terraform destroy`

- Aide

	`terraform help`
