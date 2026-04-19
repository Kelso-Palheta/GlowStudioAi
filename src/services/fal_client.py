"""
GlowStudio AI - Fal.ai Client
Direct API integration for image generation (replaces N8N image workflow).
Uses fal-ai/flux/dev/image-to-image for jewelry inpainting.
"""

import time
import requests
from typing import Dict, Any, List
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

_FAL_BASE = "https://fal.run"
_IMAGE_MODEL = "fal-ai/flux/dev/image-to-image"

# Fal.ai queue endpoint for async jobs (used for longer tasks)
_FAL_QUEUE_BASE = "https://queue.fal.run"


class FalClient:
    def __init__(self):
        self.api_key = settings.FAL_API_KEY
        self.timeout = 90

    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Key {self.api_key}",
        }

    def generate_images(
        self, prompt: str, image_base64: str, num_images: int = 2
    ) -> Dict[str, Any]:
        if not self.api_key:
            return self._mock()

        payload = {
            "prompt": prompt,
            "image_url": image_base64,
            "num_inference_steps": 28,
            "guidance_scale": 3.5,
            "strength": 0.80,
            "num_images": num_images,
            "enable_safety_checker": True,
            "output_format": "jpeg",
        }

        try:
            logger.info(f"Fal.ai: gerando {num_images} imagem(ns) — modelo={_IMAGE_MODEL}")
            url = f"{_FAL_BASE}/{_IMAGE_MODEL}"
            resp = requests.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
            resp.raise_for_status()

            data = resp.json()
            raw_images = data.get("images", [])

            if not raw_images:
                return {"success": False, "error": "Fal.ai não retornou imagens."}

            images = [
                {"url": img["url"] if isinstance(img, dict) else img, "seed": data.get("seed", 0)}
                for img in raw_images
            ]
            return {"success": True, "images": images}

        except requests.exceptions.Timeout:
            logger.error("Timeout no Fal.ai")
            return {"success": False, "error": "Fal.ai demorou demais para gerar a imagem (timeout)."}
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else "?"
            logger.error(f"Fal.ai HTTP {status}: {e}")
            return {"success": False, "error": f"Erro na API Fal.ai (HTTP {status}). Verifique sua FAL_API_KEY."}
        except Exception as e:
            logger.error(f"Erro no Fal.ai: {e}")
            return {"success": False, "error": str(e)}

    def _mock(self) -> Dict[str, Any]:
        logger.info("Fal.ai: modo mock ativo (FAL_API_KEY não configurada)")
        time.sleep(2)
        return {
            "success": True,
            "images": [
                {
                    "url": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800",
                    "seed": 42,
                },
                {
                    "url": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=800",
                    "seed": 43,
                },
            ],
        }


fal_client = FalClient()
