# Azure infrastructure

`az deployment group create --resource-group <resource-group> --template-file infra-azure/main.bicep --parameters prefix=<globally-unique-short-prefix>`

This Bicep provisions Storage (private blob container + queue), Cosmos DB, Log Analytics, Container Apps environment and ACR. It **does not** deploy the app, create AI resources/model deployments, configure Entra app registrations, or create an Azure Functions hosting plan. Those require subscription- and tenant-specific configuration; follow `docs/azure-deployment-runbook.md`. Do not interpret a successful Bicep deployment as an operational application.
