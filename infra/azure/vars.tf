variable "location" {
  type = string
  default = "westeurope"
}

variable node_type {
  type = string
  default = "Standard_D2_v2"
}

variable "node_pool_name" {
  type = string
  default = "nodepool"
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
