resource "random_password" "cluster-pw" {
  length = 32
  special = true
}

resource "azuread_application" "cluster-application" {
  name = "arkivverket-cluster"
  available_to_other_tenants = false
}

resource "azuread_service_principal" "cluster-principal" {
  application_id = azuread_application.cluster-application.application_id
}

resource "azuread_service_principal_password" "cluster-principal-pw" {
  service_principal_id = azuread_service_principal.cluster-principal.id
  value = random_password.cluster-pw.result
  end_date_relative = "8760h" # 1y
}
