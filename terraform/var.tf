variable "os_auth_url" {
    description = "The endpoint url to connect to OpenStack."
    default = "https://genostack-api-keystone.genouest.org/v3"
}
variable "os_project_id" {
    description = "The ID of the Tenant."
    default = "d84c93cbdb4e4b0a8a91ecdc4e7254f4"
}
variable "os_project_name" {
    description = "The name of the Tenant."
    default = "rdallet"
}
variable "os_user_domain_name" {    
    description = "The user domain name."    
    default = "Users"
}
variable "os_project_domain_id" {    
    description = "The project domain ID."    
    default = "0de861d3d0fc43eabf692d6dbb1cc257"
}
variable "os_user_name" {
    description = "The username for the Tenant."
    default = "rdallet" 
}
variable "os_password" {
    description = "The user password"
}
variable "tenant_network" {    
    description = "The network to be used."    
    default = "provider"
}

