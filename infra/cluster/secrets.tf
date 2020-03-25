resource "random_password" "password" {
  length = 16
  special = true
}

resource "azurerm_key_vault_secret" "db_admin_password" {
  name = "${var.cluster_name}-db-password"
  value = random_password.password.result
}

