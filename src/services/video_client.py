"""
GlowStudio AI - Video Client
Direct API integration for video generation via Kling (through Fal.ai).
Replaces N8N video workflow.
"""

import time
import requests
from typing import Dict, Any
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

_FAL_BASE = "https://fal.run"
_VIDEO_MODEL = "fal-ai/kling-video/v1/standard/image-to-video"


class VideoClient:
    def __init__(self):
        self.api_key = settings.FAL_API_KEY
        self.timeout = 180

    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Key {self.api_key}",
        }

    def generate_video(self, image_url: str, prompt: str) -> Dict[str, Any]:
        if not self.api_key:
            return self._mock()

        payload = {
            "image_url": image_url,
            "prompt": f"{prompt}, smooth elegant movement, luxury jewelry showcase, cinematic",
            "duration": "5",
            "aspect_ratio": "9:16",
        }

        try:
            logger.info(f"Kling (via Fal.ai): gerando vídeo — modelo={_VIDEO_MODEL}")
            url = f"{_FAL_BASE}/{_VIDEO_MODEL}"
            resp = requests.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
            resp.raise_for_status()

            data = resp.json()
            video = data.get("video", {})
            video_url = video.get("url") if isinstance(video, dict) else data.get("video_url")

            if not video_url:
                return {"success": False, "error": "Kling não retornou URL do vídeo."}

            return {"success": True, "video_url": video_url}

        except requests.exceptions.Timeout:
            logger.error("Timeout no Kling/Fal.ai")
            return {"success": False, "error": "A geração de vídeo excedeu o tempo limite (3 min)."}
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else "?"
            logger.error(f"Kling HTTP {status}: {e}")
            return {"success": False, "error": f"Erro na API Kling (HTTP {status}). Verifique sua FAL_API_KEY."}
        except Exception as e:
            logger.error(f"Erro no Kling: {e}")
            return {"success": False, "error": str(e)}

    def _mock(self) -> Dict[str, Any]:
        logger.info("Kling: modo mock ativo (FAL_API_KEY não configurada)")
        time.sleep(3)
        return {
            "success": True,
            "video_url": None,
            "message": "⏳ Vídeo simulado. Configure FAL_API_KEY no .env para ativar.",
        }


video_client = VideoClient()
