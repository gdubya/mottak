resource "azurerm_resource_group" "mottak-cluster" {
  location = var.location
  name = "mottak-cluster"
}

resource "azurerm_kubernetes_cluster" "mottak-cluster" {
  name = "mottak-cluster"
  location = var.location
  resource_group_name = azurerm_resource_group.mottak-cluster.name
  dns_prefix = ""

  agent_pool_profile {}
  service_principal {}
}

output "client_certificate" {
  value = azurerm_kubernetes_cluster.mottak-cluster.kube_config.0.client_certificate
}

output "kube_config" {
   value = azurerm_kubernetes_cluster.mottak-cluster.kube_config_raw
}
