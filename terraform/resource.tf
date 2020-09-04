resource "openstack_compute_instance_v2" "GGA" {
    name            = "GGA"
    image_name      = "Debian10"
    flavor_name     = "m1.medium"
    key_pair        = "local-rdallet"
    security_groups = ["default"]

    network {
        name = var.tenant_network
    }
}
