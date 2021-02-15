# TERRAFORM

Tutorial :
https://learn.hashicorp.com/terraform/getting-started/install


## What is Terraform ?

Terraform is a tool that allows us to declare, via our code, what we want for our infrastructure. 

We can automatically manage our infrastructure without manual action throught structured configuration files, whether it is the initial supply, the update or the destruction of the infrastructure.

Terraform opts for the declarative way. We declare in the configuration files the desired state of the infrastructure and Terraform will only perform minimal execution to achieve the desired state.


## How does it works ?


Terraform opts for the "push" approach. It will take the state declared in the configuration files and push the modifications to the destination provider.

Terraform is not limited to a provider (Amazon WS) or to the Cloud in general. Almost any type of infrastructure can be represented as a resource in Terraform. From docker containers on a local machine to a cloud account on DigitalOcean.


### Blocs

- provider.tf

The provider block configures the named provider, in our case openstack, which is responsible for the creation and management of resources.

https://www.terraform.io/docs/providers/index.html

- resource.tf

Le bloc ressource défini une partie de l'infrastructure. Une ressource peut être un composant physique ou une ressource logique.

https://www.terraform.io/docs/configuration/resources.html

- variables.tf

The variable block defines all the variables used. It is divided into 2 types:

1. Inputs

The inputs are used to define values ​​that configure the infrastructure. These values ​​can be used repeatedly without having to remember each of their occurrences in case they need to be updated.

2. Outputs

On the other hand, the outputs are used to obtain information on the infrastructure after deployment. These can be useful for passing information such as IP addresses for connection to the server.

https://upcloud.com/community/tutorials/terraform-variables/


## Installation (Linux)

- Add the GPG HashiCorp key :

        `curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -`

- Add the official Linux HashiCorp repository :

        `sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"`

- Update and install terraform :

	`sudo apt-get update && sudo apt-get install terraform`


## Configurations

The majority of configurations can be retrieved from the Genouest cloud in this case.

### Provider

The provider's configurations can be obtained by connecting to the account of the user on which you want to install an instance, then in the "user" panel in the upper right corner, downloading the "OpenStack RC v3 file".

- auth_url : The authentication URL
- tenant_id : The project id (tenant (v2) = project (v3))
- tenant_name : The project name
- user_domain_name : The user domain name
- project_domain_id : The project domain id
- user_name : The user name to connect with
- password : The user password to connect with


### Resource

Resource configurations can be found by logging into the user account in:
"Project -> Compute -> Images" for the image name desired.
"Project -> Compute -> Instance -> Lancer une instance -> Gabarit" for the flavor list available.
"Project -> Network -> Networks" for the network name.

- name : Instance name
- image_name : Image name to installed
- flavor_name : Flavor name
- network { name } : Network name


## Commands

- Initialization of a terraform working directory

	`terraform init`
	
- Validation of configuration files

	`terraform validate`

- Generate and display the execution plan

	`terraform plan`
	
- Apply the infrastructure modifications

	`terraform apply`
	
- Inspect the infrastructure status

	`terraform show`
	
- Delete the infrastructure

	`terraform destroy`

- Help

	`terraform help`
