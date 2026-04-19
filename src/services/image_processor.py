"""
============================================
GlowStudio AI - Image Processor
============================================
Skill 4: Especialista em IA Generativa
Skill 2: Engenheiro de Integração

Responsável por preparar a imagem da semijoia para as APIs de IA,
garantindo otimização de tamanho, redimensionamento mantendo proporção
e conversão para Base64.
"""

import base64
import io
from PIL import Image
from src.utils.logger import get_logger

logger = get_logger(__name__)

def resize_image(image_bytes: bytes, max_size: int = 1024) -> bytes:
    """
    Redimensiona a imagem mantendo a proporção (Skill 4).
    Assegura que a imagem não ultrapasse o max_size para otimizar o custo 
    e o tempo de processamento nas APIs de Inpainting (Fal.ai).
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        
        # Converte para RGB se necessário (remover canal alpha para JPG/IA compatibility)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        # Calcula nova dimensão
        width, height = img.size
        if max(width, height) > max_size:
            if width > height:
                new_width = max_size
                new_height = int(height * (max_size / width))
            else:
                new_height = max_size
                new_width = int(width * (max_size / height))
            
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            logger.info(f"Imagem redimensionada de {width}x{height} para {new_width}x{new_height}")
        
        # Salva em memória
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=90)
        return img_byte_arr.getvalue()
        
    except Exception as e:
        logger.error(f"Erro ao redimensionar imagem: {str(e)}")
        return image_bytes

def to_base64(image_bytes: bytes) -> str:
    """
    Converte bytes da imagem para string Base64 (Skill 2).
    Utilizado para compor o payload JSON dos webhooks do n8n.
    """
    try:
        base64_string = base64.b64encode(image_bytes).decode('utf-8')
        return f"data:image/jpeg;base64,{base64_string}"
    except Exception as e:
        logger.error(f"Erro na conversão Base64: {str(e)}")
        return ""

if __name__ == "__main__":
    # Teste simples (Skill Context)
    logger.info("Iniciando auto-teste de processamento de imagem...")
    # Aqui poderia ter um mock de bytes para teste unitário
