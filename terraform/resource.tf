resource "openstack_compute_instance_v2" "test" {
    name            = "test-vm"
    image_name      = "Debian9+Docker"
    flavor_name     = "m1.medium"

    network {
        name = var.tenant_network
    }
}
