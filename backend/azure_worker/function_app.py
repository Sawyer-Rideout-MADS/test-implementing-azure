import json
import logging
from functools import lru_cache
from uuid import UUID
import azure.functions as func
from app.config import Settings
from app.azure_runtime import create_azure_service

app=func.FunctionApp()
@lru_cache(maxsize=1)
def service():return create_azure_service(Settings(),worker=True)

@app.queue_trigger(arg_name='message',queue_name='%AZURE_QUEUE_NAME%',connection='AzureWebJobsStorage')
def analyze(message:func.QueueMessage):
    try:
        payload=json.loads(message.get_body())
        case_id=str(UUID(payload['case_id']))
        run_id=str(UUID(payload['run_id']))
    except Exception:raise ValueError('Invalid queue message') from None
    service().process(case_id,run_id)
