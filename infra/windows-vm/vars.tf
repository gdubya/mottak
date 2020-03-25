variable "location" {
  type = string
  default = "norwayeast"
}

variable "vm_name" {
  type = string
}

variable "vm_size" {
  type = string
  default = "Standard_B1ms"
}

variable "admin_username" {
  type = string
}

variable "admin_password" {
  type = string
}

variable "storage_account" {
  type = string
  default = "arkivverketwinshare"
}

variable "file_share_name" {
  type = string
  default = "winshare"
}

variable "file_share_quota" {
  type = number
  default = 5 # size in gigabytes
}
