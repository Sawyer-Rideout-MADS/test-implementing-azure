from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import Settings
from app.azure_runtime import create_azure_service
from app.routes.api import router
from app.services.cases import CaseError
from app.providers.interfaces import ProviderError

def create_azure_app(settings=None):
    settings=settings or Settings()
    app=FastAPI(title='ClearPath Azure')
    app.state.settings=settings
    app.state.service=create_azure_service(settings)
    app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in settings.cors_allowed_origins.split(',') if x.strip()],allow_methods=['GET','POST','PUT'],allow_headers=['Authorization','Content-Type'])
    @app.exception_handler(CaseError)
    async def case_error(request:Request,exc:CaseError):return JSONResponse(status_code=exc.status,content={'detail':str(exc)})
    @app.exception_handler(ProviderError)
    async def provider_error(request:Request,exc:ProviderError):return JSONResponse(status_code=503,content={'detail':'A provider is unavailable.'})
    app.include_router(router,prefix='/api')
    return app

app=create_azure_app()
