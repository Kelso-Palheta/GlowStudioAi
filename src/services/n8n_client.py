"""
============================================
GlowStudio AI - n8n Client
============================================
Skill 2: Engenheiro de Integração
Skill 3: Estratégia e Copywriting (Mocks)

Cliente para comunicação com os webhooks do n8n.
Gerencia as chamadas de geração de texto (Maritaca AI) e imagem (Fal.ai).
"""

import requests
import json
import time
from typing import Dict, Any, Optional
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class N8NClient:
    def __init__(self):
        self.base_url = settings.N8N_BASE_URL
        # Aumentamos o timeout para lidar com a latência de geração de IA
        self.timeout = 150  # 2.5 minutos
        self.mock_mode = settings.APP_ENV == "development"
        self._api_key = settings.N8N_API_KEY

    def _get_headers(self) -> Dict[str, str]:
        """Gera os headers de autenticação (Skill 2)."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
            headers["X-API-Key"] = self._api_key
        return headers

    def generate_content(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Envia dados para o webhook do n8n para geração de texto (Maritaca AI).
        (Skill 2)
        """
        # Fallback para Mock se a URL estiver vazia ou for inválida em desenvolvimento
        is_url_invalid = not settings.N8N_WEBHOOK_TEXT or not settings.N8N_WEBHOOK_TEXT.startswith("http")
        if self.mock_mode and is_url_invalid:
            return self._generate_content_mock(payload)
        
        try:
            logger.info(f"Chamando n8n (Maritaca AI): {settings.N8N_WEBHOOK_TEXT}")
            response = requests.post(
                settings.N8N_WEBHOOK_TEXT,
                json=payload,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            # Validação básica do retorno esperado no PRD
            if "legenda" in data and "prompt_visual" in data:
                return {"success": True, **data}
            
            logger.warning(f"Resposta do n8n incompleta: {data}")
            return {"success": False, "error": "Resposta incompleta do orquestrador."}
            
        except requests.exceptions.Timeout:
            logger.error("Timeout na chamada ao n8n (Maritaca AI)")
            return {"success": False, "error": "O servidor demorou muito para responder (Timeout)."}
        except Exception as e:
            logger.error(f"Erro na conexão com n8n: {str(e)}")
            return {"success": False, "error": f"Falha na conexão: {str(e)}"}

    def generate_images(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Envia dados para o webhook do n8n para geração de imagem (Fal.ai).
        (Skill 2)
        """
        is_url_invalid = not settings.N8N_WEBHOOK_IMAGE or not settings.N8N_WEBHOOK_IMAGE.startswith("http")
        if self.mock_mode and is_url_invalid:
            return self._generate_images_mock(payload.get("prompt", ""))
        
        try:
            logger.info(f"Chamando n8n (Fal.ai): {settings.N8N_WEBHOOK_IMAGE}")
            response = requests.post(
                settings.N8N_WEBHOOK_IMAGE,
                json=payload,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            # O retorno pode ser uma lista de imagens ou uma URL
            if "images" in data or "url" in data:
                return {"success": True, **data}
            
            return {"success": False, "error": "Falha ao receber imagens da IA."}
            
        except Exception as e:
            logger.error(f"Erro na geração de imagem n8n: {str(e)}")
            return {"success": False, "error": str(e)}

    def _generate_content_mock(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Simulação Maritaca AI (Skill 3)."""
        logger.info("Modo MOCK: Simulação Maritaca AI ativa.")
        time.sleep(2)
        # ... (mantém a lógica anterior de mock)
        objetivo = payload.get("objetivo", "Venda")
        publico = payload.get("publico", "Geral")
        diferenciais = ", ".join(payload.get("diferenciais", []))

        mock_legenda = (
            f"✨ **Beleza e Sofisticação para {publico}** ✨\n\n"
            f"Essa semijoia foi selecionada com foco em {objetivo.lower()}, "
            f"trazendo a exclusividade que você procura.\n\n"
            f"💎 **Diferenciais:** {diferenciais}\n"
            f"🛍️ Garanta a sua agora!\n\n"
            f"#Semijoias #LuxoAcessivel"
        )

        mock_prompt_visual = "Luxury jewelry model, professional studio lighting, 8k."

        return {
            "success": True,
            "legenda": mock_legenda,
            "prompt_visual": mock_prompt_visual
        }

    def _generate_images_mock(self, prompt: str) -> Dict[str, Any]:
        """Simulação Fal.ai (Skill 4)."""
        logger.info("Modo MOCK: Simulação Fal.ai ativa.")
        time.sleep(3)
        return {
            "success": True,
            "images": [
                {"url": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800", "seed": 123}
            ]
        }

    def generate_video(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Envia imagem para o webhook do n8n para animação de vídeo (Kling/Hedra).
        (Skill 4: Engenharia de Mídia)
        """
        is_url_invalid = not settings.N8N_WEBHOOK_VIDEO or not settings.N8N_WEBHOOK_VIDEO.startswith("http")
        if self.mock_mode and is_url_invalid:
            return self._generate_video_mock()
        
        try:
            logger.info(f"Chamando n8n (Kling/Hedra): {settings.N8N_WEBHOOK_VIDEO}")
            response = requests.post(
                settings.N8N_WEBHOOK_VIDEO,
                json=payload,
                headers=self._get_headers(),
                timeout=self.timeout * 2  # Vídeo pode demorar mais
            )
            response.raise_for_status()
            
            data = response.json()
            if "video_url" in data or "video" in data:
                return {"success": True, **data}
            
            return {"success": False, "error": "Resposta de vídeo inválida."}
            
        except requests.exceptions.Timeout:
            logger.error("Timeout na geração de vídeo")
            return {"success": False, "error": "A geração de vídeo excedeu o tempo limite."}
        except Exception as e:
            logger.error(f"Erro na geração de vídeo: {str(e)}")
            return {"success": False, "error": str(e)}

    def _generate_video_mock(self) -> Dict[str, Any]:
        """Simulação Kling/Hedra (Skill 4)."""
        logger.info("Modo MOCK: Simulação Kling/Hedra ativa.")
        time.sleep(4)
        return {
            "success": True,
            "video_url": None,  # Sem vídeo real no mock
            "message": "⏳ Geração de vídeo simulada. Conecte o webhook N8N_WEBHOOK_VIDEO para ativar."
        }

# Singleton para uso no app
n8n_client = N8NClient()

