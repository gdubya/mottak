variable "resource_group_name" {
  type = string
  default = "arkivverket"
}

variable "storage_account_name" {
  type = string
  default = "arkivverketstorage"
}

variable "tfstate_container_name" {
  type = string
  default = "tfstate"
}

variable "location" {
  type = string
  default = "norwayeast"
}

variable node_type {
  type = string
  default = "Standard_D2_v2"
}

variable "node_count" {
  type = number
  default = 2
}

variable "max_node_count" {
  type = number
  default = 8
}

variable "min_node_count" {
  type = number
  default = 1
}

variable "dns_prefix" {
  type = string
  default = "arkivverket"
}

variable "db_admin_name" {
  type = string
  default = "postgres"
}

variable "cluster_name" {
  type = string
}

