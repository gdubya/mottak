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
    storage_account_name = "arkivverketmottak" # the storage account is created in advance, outside of terraform
    resource_group_name = "terraform"
    container_name = "tfstate"

    key = "terraform.tfstate"
  }
}

