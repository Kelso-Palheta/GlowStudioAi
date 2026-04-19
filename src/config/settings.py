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
    # --- Aplicação ---
    APP_NAME: str = os.getenv("APP_NAME", "GlowStudio AI")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_DEBUG: bool = os.getenv("APP_DEBUG", "true").lower() == "true"
    APP_PORT: int = int(os.getenv("APP_PORT", "8501"))
    APP_SECRET_KEY: str = os.getenv("APP_SECRET_KEY", "")

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
        """Valida configurações obrigatórias em produção. Retorna lista de erros."""
        errors = []
        if self.is_production:
            if not self.APP_SECRET_KEY:
                errors.append("APP_SECRET_KEY é obrigatório em produção.")
            if not self.MARITACA_API_KEY:
                errors.append("MARITACA_API_KEY é obrigatória para geração de texto.")
            if not self.FAL_API_KEY:
                errors.append("FAL_API_KEY é obrigatória para geração de imagem e vídeo.")
        return errors


# Singleton
settings = _Settings()
