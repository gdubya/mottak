resource "azurerm_container_registry" "mottak-cr" {
  location = var.location
  name = "mottakcr"
  resource_group_name = azurerm_resource_group.mottak-cluster.name
  admin_enabled = false
  sku = "Standard"
}
