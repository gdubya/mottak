resource "azurerm_virtual_network" "vm-network" {
  name                = "${var.vm_name}-network"
  location            = var.location
  resource_group_name = "arkivverket"
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "vm-subnet" {
  name                 = "${var.vm_name}-subnet"
  resource_group_name  = "arkivverket"
  virtual_network_name = azurerm_virtual_network.vm-network.name
  address_prefix       = "10.0.0.0/24"
}

resource "azurerm_public_ip" "vm_public_ip" {
    name                         = "${var.vm_name}-public-ip"
    location                     = var.location
    resource_group_name          = "arkivverket"
    allocation_method            = "Dynamic"
}
