resource "random_password" "mottak-cluster-pw" {
  length = 32
  special = true
}

resource "azuread_application" "mottak-cluster" {
  name = "mottak-cluster"
  available_to_other_tenants = false
}

resource "azuread_service_principal" "mottak-cluster" {
  application_id = azuread_application.mottak-cluster.application_id
}

resource "azuread_service_principal_password" "mottak-cluster" {
  service_principal_id = azuread_service_principal.mottak-cluster.id
  value = random_password.mottak-cluster-pw.result
  end_date_relative = "8760h" # 1y
}
