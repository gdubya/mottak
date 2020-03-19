resource "azurerm_virtual_machine" "machine-instance" {
  name                  = var.vm_name
  location              = var.location
  resource_group_name   = "arkivverket"
  network_interface_ids = [azurerm_network_interface.vm_nic.id]
  vm_size               = var.vm_size

  delete_os_disk_on_termination = true
  delete_data_disks_on_termination = false

  storage_image_reference {
    publisher = "MicrosoftWindowsDesktop"
    offer     = "Windows-10"
    sku       = "19h1-ent"
    version   = "latest"
  }

  storage_os_disk {
    name              = "${var.vm_name}-osdisk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  os_profile {
    computer_name  = var.vm_name
    admin_username = var.admin_username
    admin_password = var.admin_password
  }

  os_profile_windows_config {
    provision_vm_agent = true
  }
}

resource "azurerm_network_interface" "vm_nic" {
  name                      = "${var.vm_name}-nic"
  location                  = var.location
  resource_group_name       = "arkivverket"

  ip_configuration {
    name                          = "vmipcfg"
    subnet_id                     = azurerm_subnet.vm-subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.vm_public_ip.id
  }
}


# Workaround for https://github.com/terraform-providers/terraform-provider-azurerm/issues/764
data "azurerm_public_ip" "vm_public_ip" {
    name                         = azurerm_public_ip.vm_public_ip.name
    resource_group_name          = azurerm_virtual_machine.machine-instance.resource_group_name
}

output "public_ip_address" {
  value = data.azurerm_public_ip.vm_public_ip.ip_address
}
