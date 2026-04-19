"""
============================================
GlowStudio AI - Validators
============================================
Validação de inputs e arquivos de upload.
Segue regras de segurança do Documento Mestre (Seção 2 e 8.3).
"""

from dataclasses import dataclass
from typing import Optional
from streamlit.runtime.uploaded_file_manager import UploadedFile


# MIME types permitidos para imagens
_ALLOWED_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/webp",
}

# Extensões permitidas
_ALLOWED_EXTENSIONS = {
    "png", "jpg", "jpeg", "webp",
}


@dataclass
class ValidationResult:
    """Resultado de uma validação."""
    is_valid: bool
    error_message: Optional[str] = None


def validate_image(file: Optional[UploadedFile]) -> ValidationResult:
    """Valida um arquivo de imagem enviado pelo usuário.
    
    Verifica:
    1. Se o arquivo existe
    2. Tipo MIME do arquivo
    3. Extensão do arquivo
    4. Tamanho máximo (configurável via .env)
    
    Args:
        file: Arquivo enviado via st.file_uploader
        
    Returns:
        ValidationResult com is_valid e mensagem de erro se inválido.
        
    Exemplo:
        >>> result = validate_image(uploaded_file)
        >>> if not result.is_valid:
        ...     st.error(result.error_message)
    """
    # Importar settings aqui para evitar circular import
    from src.config.settings import settings

    # 1. Arquivo existe?
    if file is None:
        return ValidationResult(
            is_valid=False,
            error_message="Nenhum arquivo selecionado. Faça upload de uma imagem.",
        )

    # 2. Tipo MIME válido?
    if file.type not in _ALLOWED_MIME_TYPES:
        return ValidationResult(
            is_valid=False,
            error_message=(
                f"Tipo de arquivo não permitido: {file.type}. "
                f"Use: PNG, JPG ou WEBP."
            ),
        )

    # 3. Extensão válida?
    file_extension = file.name.rsplit(".", 1)[-1].lower() if "." in file.name else ""
    if file_extension not in _ALLOWED_EXTENSIONS:
        return ValidationResult(
            is_valid=False,
            error_message=(
                f"Extensão não permitida: .{file_extension}. "
                f"Use: .png, .jpg, .jpeg ou .webp."
            ),
        )

    # 4. Tamanho dentro do limite?
    if file.size > settings.UPLOAD_MAX_SIZE_BYTES:
        max_mb = settings.UPLOAD_MAX_SIZE_MB
        file_mb = round(file.size / (1024 * 1024), 1)
        return ValidationResult(
            is_valid=False,
            error_message=(
                f"Arquivo muito grande: {file_mb}MB. "
                f"O tamanho máximo permitido é {max_mb}MB."
            ),
        )

    return ValidationResult(is_valid=True)
