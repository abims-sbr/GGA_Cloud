# Configure the OpenStack Provider
provider "openstack" {
    auth_url = var.os_auth_url
    tenant_id = var.os_project_id
    tenant_name = var.os_project_name
    user_domain_name = var.os_user_domain_name
    project_domain_id = var.os_project_domain_id
    user_name = var.os_user_name
    password = var.os_password
}
