terraform {
  required_providers {
    openstack = {
      source = "terraform-provider-openstack/openstack"
    }
  }
}

resource "openstack_compute_instance_v2" "GGA" {
    name            = "GGA"
#    image_name      = "Debian10"
    image_id        = "f7be72a3-1765-4212-8094-59c442201cb2"
    flavor_name     = "m1.medium"
    key_pair        = "rdallet-sbr"
    security_groups = ["default"]

    network {
        name = var.tenant_network
    }
}
