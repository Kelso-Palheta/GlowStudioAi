"""
============================================
GlowStudio AI - Settings
============================================
Carregamento seguro de variáveis de ambiente.
Segue Protocolo de Segurança do Documento Mestre (Seção 2).
"""

import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Carregar .env da raiz do projeto
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_ENV_PATH = _PROJECT_ROOT / ".env"

if _ENV_PATH.exists():
    load_dotenv(_ENV_PATH, override=True)


class _Settings:
    def _get_clean_env(self, key: str, default: str = "") -> str:
        """Obtém variável de ambiente e remove espaços e comentários residuais."""
        val = os.getenv(key, default).strip()
        # Se a string começar com # ou for apenas o comentário do .env.example, retorna o padrão
        if val.startswith("#") or "URL do webhook" in val:
            return default
        return val

    # --- Aplicação ---
    APP_NAME: str = os.getenv("APP_NAME", "GlowStudio AI")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_DEBUG: bool = os.getenv("APP_DEBUG", "true").lower() == "true"
    APP_PORT: int = int(os.getenv("APP_PORT", "8501"))
    APP_SECRET_KEY: str = os.getenv("APP_SECRET_KEY", "")

    # --- n8n ---
    N8N_BASE_URL: str = os.getenv("N8N_BASE_URL", "http://localhost:5678")
    N8N_WEBHOOK_TEXT: str = "" # Inicializada abaixo
    N8N_WEBHOOK_IMAGE: str = ""
    N8N_WEBHOOK_VIDEO: str = ""
    N8N_API_KEY: str = os.getenv("N8N_API_KEY", "")
    N8N_TIMEOUT_SECONDS: int = int(os.getenv("N8N_TIMEOUT_SECONDS", "120"))

    def __init__(self):
        # Carregamento com limpeza de comentários acidentais
        self.N8N_WEBHOOK_TEXT = self._get_clean_env("N8N_WEBHOOK_TEXT", "")
        self.N8N_WEBHOOK_IMAGE = self._get_clean_env("N8N_WEBHOOK_IMAGE", "")
        self.N8N_WEBHOOK_VIDEO = self._get_clean_env("N8N_WEBHOOK_VIDEO", "")

    # --- Maritaca AI ---
    MARITACA_API_KEY: str = os.getenv("MARITACA_API_KEY", "")
    MARITACA_MODEL: str = os.getenv("MARITACA_MODEL", "sabia-3")

    # --- Fal.ai ---
    FAL_API_KEY: str = os.getenv("FAL_API_KEY", "")

    # --- Supabase (Banco de Dados / Auth) ---
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

    # --- Upload ---
    UPLOAD_MAX_SIZE_MB: int = int(os.getenv("UPLOAD_MAX_SIZE_MB", "10"))
    UPLOAD_MAX_SIZE_BYTES: int = UPLOAD_MAX_SIZE_MB * 1024 * 1024
    UPLOAD_ALLOWED_EXTENSIONS: List[str] = os.getenv(
        "UPLOAD_ALLOWED_EXTENSIONS", "png,jpg,jpeg,webp"
    ).split(",")

    # --- Logs ---
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # --- Paths ---
    PROJECT_ROOT: Path = _PROJECT_ROOT
    ASSETS_DIR: Path = _PROJECT_ROOT / "assets"
    CSS_DIR: Path = _PROJECT_ROOT / "assets" / "css"

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    def validate(self) -> List[str]:
        """Valida configurações obrigatórias. Retorna lista de erros. (Skill 5)"""
        errors = []
        if self.is_production:
            if not self.APP_SECRET_KEY:
                errors.append("APP_SECRET_KEY é obrigatório em produção.")
            if not self.N8N_WEBHOOK_TEXT:
                errors.append("N8N_WEBHOOK_TEXT (Maritaca AI) é obrigatório em produção.")
            if not self.N8N_WEBHOOK_IMAGE:
                errors.append("N8N_WEBHOOK_IMAGE (Fal.ai) é obrigatório em produção.")
            if not self.FAL_API_KEY:
                errors.append("FAL_API_KEY é recomendada para geração de imagem.")
        
        # Validação de formato básico de URL
        for key, url in [
            ("N8N_WEBHOOK_TEXT", self.N8N_WEBHOOK_TEXT),
            ("N8N_WEBHOOK_IMAGE", self.N8N_WEBHOOK_IMAGE)
        ]:
            if url and not url.startswith("http"):
                errors.append(f"{key} deve ser uma URL válida começando com http/https.")
                
        return errors


# Singleton
settings = _Settings()
