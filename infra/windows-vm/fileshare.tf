resource "azurerm_storage_account" "storage_account" {
  name                     = var.storage_account
  resource_group_name      = "arkivverket"
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_share" "fileshare" {
  name = var.file_share_name
  storage_account_name = azurerm_storage_account.storage_account.name
  quota = var.file_share_quota
}

