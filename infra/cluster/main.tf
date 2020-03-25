provider "azurerm" {
  version = "~>1.5"
}

provider "azuread" {
  version = "~> 0.7"
}

provider "random" {
  version = "~> 2.2"
}

terraform {
  backend "azurerm" {
    # Created elsewhere (outside of terraform)
    storage_account_name = "arkivverketstorage"
    resource_group_name = var.resource_group_name
    container_name = "tfstate"

    key = "terraform.tfstate"
  }
}

