from app.config import Settings
from app.providers.interfaces import Providers
from app.providers.azure.adapters import (AzureBlobDocuments,AzureDocumentExtractor,AzurePrivacyFilter,
    AzureExplanations,CosmosCases,CosmosMemory,AzureQueueDispatcher)
from app.services.cases import CaseService

def create_azure_service(settings:Settings,worker=False):
    if settings.app_mode!='azure':raise ValueError('Azure mode required')
    settings.validate_mode(worker=worker)
    return CaseService(Providers(extraction=AzureDocumentExtractor(settings),privacy=AzurePrivacyFilter(settings),
        explanations=AzureExplanations(settings),documents=AzureBlobDocuments(settings),
        cases=CosmosCases(settings),memory=CosmosMemory(settings),
        dispatcher=None if worker else AzureQueueDispatcher(settings)))
