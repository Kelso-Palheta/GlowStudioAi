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
_TEXT_TO_IMAGE_MODEL = "fal-ai/flux/dev"
_FACE_ID_MODEL = "fal-ai/ip-adapter-face-id"


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

    def generate_model_from_text(self, description: str, num_images: int = 1) -> Dict[str, Any]:
        """Generates a model headshot from a text description (Etapa 0 — Minha Modelo)."""
        if not self.api_key:
            return self._mock()

        prompt = (
            f"{description}, professional headshot, clean white background, "
            "photorealistic, 8k, commercial photography, sharp focus"
        )
        payload = {
            "prompt": prompt,
            "negative_prompt": "ugly, blurry, low quality, deformed, multiple people",
            "num_inference_steps": 28,
            "guidance_scale": 3.5,
            "num_images": num_images,
            "image_size": "portrait_4_3",
            "enable_safety_checker": True,
            "output_format": "jpeg",
        }

        try:
            logger.info(f"Fal.ai: gerando modelo por texto — modelo={_TEXT_TO_IMAGE_MODEL}")
            url = f"{_FAL_BASE}/{_TEXT_TO_IMAGE_MODEL}"
            resp = requests.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            images = data.get("images", [])
            if not images:
                return {"success": False, "error": "Fal.ai não gerou imagens da modelo."}
            normalized = [{"url": img["url"] if isinstance(img, dict) else img, "seed": data.get("seed", 0)} for img in images]
            return {"success": True, "images": normalized}
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Timeout ao gerar modelo. Tente novamente."}
        except Exception as e:
            logger.error(f"Erro ao gerar modelo por texto: {e}")
            return {"success": False, "error": str(e)}

    def generate_model_with_face(
        self, face_image_url: str, prompt: str, num_images: int = 2
    ) -> Dict[str, Any]:
        """Step 1 of 2: Generate model with consistent face via IP-Adapter FaceID."""
        if not self.api_key:
            return self._mock()

        payload = {
            "face_image_url": face_image_url,
            "prompt": prompt,
            "negative_prompt": "ugly, blurry, low quality, deformed, extra limbs, bad anatomy",
            "scale": 0.8,
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
            "num_images": num_images,
            "enable_safety_checker": True,
            "output_format": "jpeg",
        }

        try:
            logger.info(f"Fal.ai IP-Adapter FaceID: gerando modelo com rosto de referência")
            url = f"{_FAL_BASE}/{_FACE_ID_MODEL}"
            resp = requests.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            images = data.get("images", [])
            if not images:
                return {"success": False, "error": "IP-Adapter não retornou imagens."}
            normalized = [{"url": img["url"] if isinstance(img, dict) else img, "seed": data.get("seed", 0)} for img in images]
            return {"success": True, "images": normalized}
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Timeout no IP-Adapter. Tente novamente."}
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else "?"
            logger.error(f"IP-Adapter HTTP {status}: {e}")
            return {"success": False, "error": f"Erro no IP-Adapter (HTTP {status})."}
        except Exception as e:
            logger.error(f"Erro no IP-Adapter FaceID: {e}")
            return {"success": False, "error": str(e)}

    def apply_jewelry(
        self, model_image_url: str, jewelry_base64: str, prompt: str
    ) -> Dict[str, Any]:
        """Step 2 of 2: Apply jewelry onto generated model via image-to-image."""
        if not self.api_key:
            return self._mock()

        enhanced_prompt = (
            f"{prompt}, wearing the exact jewelry piece, precise jewelry placement, "
            "photorealistic jewelry integration, professional studio lighting, "
            "high detail jewelry texture and reflections"
        )
        payload = {
            "prompt": enhanced_prompt,
            "image_url": model_image_url,
            "strength": 0.45,
            "num_inference_steps": 28,
            "guidance_scale": 4.0,
            "num_images": 1,
            "enable_safety_checker": True,
            "output_format": "jpeg",
        }

        try:
            logger.info("Fal.ai: aplicando joia na modelo (image-to-image)")
            url = f"{_FAL_BASE}/{_IMAGE_MODEL}"
            resp = requests.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            images = data.get("images", [])
            if not images:
                return {"success": False, "error": "Inpainting não retornou imagem."}
            normalized = [{"url": img["url"] if isinstance(img, dict) else img, "seed": data.get("seed", 0)} for img in images]
            return {"success": True, "images": normalized}
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Timeout ao aplicar joia. Tente novamente."}
        except Exception as e:
            logger.error(f"Erro ao aplicar joia: {e}")
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
