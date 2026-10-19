from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]
# Synthetic sample packets ship inside the app package so the Lambda bundle
# (which copies only backend/app) includes them for "Load sample case".
SAMPLES_DIR = Path(__file__).resolve().parent / "samples"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")
    app_mode: str = "demo"
    local_data_dir: Path = ROOT / "local-data"
    cors_allowed_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    azure_storage_connection_string: str = ""
    azure_storage_container: str = "documents"
    azure_queue_name: str = "analysis-jobs"
    azure_cosmos_endpoint: str = ""
    azure_cosmos_key: str = ""
    azure_cosmos_database: str = "clearpath"
    azure_cosmos_container: str = "cases"
    azure_document_intelligence_endpoint: str = ""
    azure_document_intelligence_key: str = ""
    azure_language_endpoint: str = ""
    azure_language_key: str = ""
    azure_openai_endpoint: str = ""
    azure_openai_key: str = ""
    azure_openai_deployment: str = ""
    azure_tenant_id: str = ""
    azure_api_audience: str = ""
    aws_region: str = ""
    aws_profile: str = ""
    bedrock_model_id: str = ""
    bedrock_guardrail_id: str = ""
    bedrock_guardrail_version: str = ""
    s3_document_bucket: str = ""
    dynamodb_cases_table: str = ""
    worker_lambda_function_name: str = ""
    # Optional AgentCore Memory (long-term review lessons). Blank disables it;
    # the namespace must match the semantic strategy's template in infra.
    agentcore_memory_id: str = ""
    agentcore_memory_strategy_id: str = ""
    agentcore_memory_namespace: str = "/clearpath/lessons/{memoryStrategyId}/{actorId}/"

    def validate_mode(self, *, worker: bool = False) -> None:
        if self.app_mode not in {"demo", "aws", "azure"}:
            raise ValueError("APP_MODE must be demo, aws or azure.")
        if bool(self.agentcore_memory_id.strip()) != bool(
            self.agentcore_memory_strategy_id.strip()
        ):
            raise ValueError(
                "AGENTCORE_MEMORY_ID and AGENTCORE_MEMORY_STRATEGY_ID must be supplied together."
            )
        if self.app_mode == "azure":
            required = ["azure_storage_connection_string", "azure_cosmos_endpoint",
                        "azure_document_intelligence_endpoint", "azure_document_intelligence_key",
                        "azure_language_endpoint", "azure_language_key", "azure_openai_endpoint",
                        "azure_openai_deployment", "azure_tenant_id", "azure_api_audience"]
            missing = [key.upper() for key in required if not getattr(self, key).strip()]
            if missing:
                raise ValueError("Azure configuration missing: " + ", ".join(missing))
        if self.app_mode == "aws":
            required = [
                "aws_region",
                "bedrock_model_id",
                "bedrock_guardrail_id",
                "bedrock_guardrail_version",
                "s3_document_bucket",
                "dynamodb_cases_table",
            ]

            if not worker:
                required.append("worker_lambda_function_name")

            missing = [
                key.upper() for key in required if not getattr(self, key).strip()
            ]
            if missing:
                raise ValueError("AWS configuration missing: " + ", ".join(missing))
