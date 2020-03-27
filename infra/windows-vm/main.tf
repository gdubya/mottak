provider "azurerm" {
  version = "~>1.5"
}

provider "azuread" {
  version = "~> 0.7"
}

terraform {
  backend "azurerm" {
    # Created elsewhere (outside of terraform)
    storage_account_name = "arkivverketwin"
    resource_group_name = "arkivverket"
    container_name = "tfstate"

    key = "terraform.tfstate"
  }
}

