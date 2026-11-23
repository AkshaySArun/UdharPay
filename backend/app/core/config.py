from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")
    database_url: str = "sqlite:///./data/udharpay.db"
    sarvam_api_key: str = ""
    sarvam_base_url: str = "https://api.sarvam.ai"
    sarvam_voice_api_key: str = ""
    sarvam_voice_org_id: str = ""
    sarvam_voice_workspace_id: str = ""
    sarvam_voice_app_id: str = ""
    sarvam_voice_app_version: int = 1
    sarvam_voice_connection_id: str = ""
    sarvam_voice_agent_phone_number: str = ""
    sarvam_voice_test_phone_number: str = "+919731914376"
    cashfree_client_id: str = ""
    cashfree_client_secret: str = ""
    cashfree_environment: str = "sandbox"
    cashfree_api_version: str = "2025-01-01"
    jwt_secret_key: str = "local-development-secret-change-before-deployment"
    frontend_url: str = "http://localhost:3000"
    backend_url: str = "http://localhost:8000"
    upload_directory: str = "uploads"
    max_upload_size_mb: int = 10
    demo_mode: bool = False

settings = Settings()
