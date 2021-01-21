### The Ansible hosts file
resource "local_file" "AnsibleInventory" {
 content = templatefile("hosts.tmpl",
 {
  os_cloud_ip = var.os_auth_url,
  os_vms_ip = openstack_compute_instance_v2.GGA.access_ip_v4,
 }
 )
 filename = "hosts"
}
