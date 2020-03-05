resource "azurerm_resource_group" "mottak-cluster" {
  location = var.location
  name = "mottak-cluster"
}

resource "azurerm_kubernetes_cluster" "mottak-cluster" {
  name = "mottak-cluster"
  location = var.location
  resource_group_name = azurerm_resource_group.mottak-cluster.name
  dns_prefix = "mottak"

  service_principal {
    client_id = azuread_service_principal.mottak-cluster.application_id
    client_secret = random_password.mottak-cluster-pw.result
  }

  agent_pool_profile {
    name = var.node_pool_name
    count = var.node_count
    min_count = var.min_node_count
    max_count = var.max_node_count
    type = "VirtualMachineScaleSets"
    enable_auto_scaling = true
    vm_size = var.node_type
  }
}

output "client_certificate" {
  value = azurerm_kubernetes_cluster.mottak-cluster.kube_config.0.client_certificate
}

output "kube_config" {
   value = azurerm_kubernetes_cluster.mottak-cluster.kube_config_raw
}
