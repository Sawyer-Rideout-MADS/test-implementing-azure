@description('Deployment region (check Azure AI model availability separately).')
param location string = resourceGroup().location
@minLength(3)
@maxLength(12)
param prefix string
param tags object = { project: 'clearpath' }
var storageName = toLower('${prefix}storage')
var cosmosName = toLower('${prefix}-cosmos')
resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
 name: storageName
 location: location
 tags: tags
 sku: { name: 'Standard_LRS' }
 kind: 'StorageV2'
 properties: { allowBlobPublicAccess: false minimumTlsVersion: 'TLS1_2' }
}
resource blobs 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = { parent: storage name: 'default' }
resource docs 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
 parent: blobs name: 'documents' properties: { publicAccess: 'None' }
}
resource queues 'Microsoft.Storage/storageAccounts/queueServices@2023-05-01' = { parent: storage name: 'default' }
resource jobs 'Microsoft.Storage/storageAccounts/queueServices/queues@2023-05-01' = { parent: queues name: 'analysis-jobs' }
resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {
 name: cosmosName location: location tags: tags
 kind: 'GlobalDocumentDB'
 properties: { databaseAccountOfferType: 'Standard' locations: [{ locationName: location failoverPriority: 0 }] consistencyPolicy: { defaultConsistencyLevel: 'Session' } }
}
resource database 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-05-15' = {
 parent: cosmos name: 'clearpath' properties: { resource: { id: 'clearpath' } options: { throughput: 400 } }
}
resource cases 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = {
 parent: database name: 'cases' properties: { resource: { id: 'cases' partitionKey: { paths: ['/id'] kind: 'Hash' } } }
}
resource logs 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
 name: '${prefix}-logs' location: location tags: tags properties: { retentionInDays: 30 } sku: { name: 'PerGB2018' }
}
resource environment 'Microsoft.App/managedEnvironments@2024-03-01' = {
 name: '${prefix}-env' location: location tags: tags
 properties: { appLogsConfiguration: { destination: 'log-analytics' logAnalyticsConfiguration: { customerId: logs.properties.customerId sharedKey: listKeys(logs.id, logs.apiVersion).primarySharedKey } } }
}
resource registry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
 name: toLower('${prefix}acr') location: location tags: tags sku: { name: 'Basic' } properties: { adminUserEnabled: false }
}
output storageAccountName string = storage.name
output cosmosEndpoint string = cosmos.properties.documentEndpoint
output containerEnvironmentId string = environment.id
output registryName string = registry.name
