provider "azurerm" {
  version = "=2.0.0"
  features {}
}

terraform {
  backend "azurerm" {
    storage_account_name = "arkivverketmottak" # the storage account is created in advance, outside of terraform
    resource_group_name = "terraform"
    container_name = "tfstate"
    key = "terraform.tfstate"
  }
}

