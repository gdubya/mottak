resource "azurerm_postgresql_server" "postgres" {
  name                = "${var.cluster_name}-database"
  location            = var.location
  resource_group_name = var.resource_group_name

  storage_profile {
    storage_mb            = 10240 # 10gigs
    backup_retention_days = 7
    geo_redundant_backup  = "Disabled"
    auto_grow             = "Enabled"
  }

  administrator_login          = var.db_admin_name
  administrator_login_password = azurerm_key_vault_secret.db_admin_password.value
  version                      = "11"
  ssl_enforcement              = "Enabled"

  sku {
    name = "B_Gen5_1"
    capacity = 1
    family = "Gen5"
    tier = "Basic"
  }
}
