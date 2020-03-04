provider "azurerm" {
  version = "=2.0.0"
  features {}
}

resource "azurerm_resource_group" "terraform-state" {
  location = var.location
  name = "terraform"
}

terraform {
  backend "azurerm" {
    storage_account_name = "arkivverketmottak" # the storage account is created in advance, outside of terraform
    resource_group_name = "terraform"
    container_name = "tfstate"
    key = "terraform.tfstate"
  }
}

