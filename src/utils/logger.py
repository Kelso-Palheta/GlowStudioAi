"""
============================================
GlowStudio AI - Logger
============================================
Logging estruturado com formato padronizado.
Nível configurável via LOG_LEVEL no .env.
"""

import logging
import sys
from typing import Optional


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Retorna um logger configurado com o padrão do GlowStudio AI.
    
    Args:
        name: Nome do módulo. Se None, usa 'glowstudio'.
        
    Returns:
        Logger configurado com formato e nível do .env.
        
    Exemplo:
        >>> from src.utils import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Imagem processada com sucesso")
    """
    # Importar settings aqui para evitar circular import
    from src.config.settings import settings

    logger_name = name or "glowstudio"
    logger = logging.getLogger(logger_name)

    # Evitar adicionar handlers duplicados
    if not logger.handlers:
        logger.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))

        # Handler para stdout
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))

        # Formato: [2026-04-12 21:30:00] [INFO] [module] — mensagem
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s] — %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Não propagar para o logger raiz
        logger.propagate = False

    return logger
