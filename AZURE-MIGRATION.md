# Azure migration

The Azure implementation is under `backend/app/providers/azure`, `backend/app/azure_api.py`, `backend/azure_worker`, and `infra-azure`. The frontend supports `VITE_AUTH_MODE=entra` with PKCE. The existing AWS and demo modes are retained for reference and local regression.

**Start here:** `docs/azure-deployment-runbook.md` and the two `.env.azure.example` files. The repository has not been deployed or end-to-end tested against an Azure subscription. Do not use real client information until security/privacy validation is complete.
