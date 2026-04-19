"""
GlowStudio AI - AI Pipeline
Orchestrates direct calls to Maritaca AI, Fal.ai, and Kling.
Replaces the N8N middleware layer. Public interface is unchanged.
"""

from typing import Dict, Any, List
from src.services.maritaca_client import maritaca_client
from src.services.fal_client import fal_client
from src.services.video_client import video_client
from src.utils.logger import get_logger

logger = get_logger(__name__)


class AIPipeline:
    """Drop-in replacement for N8NClient. Views import this as n8n_client."""

    def generate_content(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Generates marketing text + visual prompt via Maritaca AI."""
        return maritaca_client.generate_content(
            objetivo=payload.get("objetivo", ""),
            publico=payload.get("publico", ""),
            diferenciais=payload.get("diferenciais", []),
            cenario=payload.get("cenario", ""),
            look=payload.get("look", ""),
        )

    def generate_images(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates product images via Fal.ai.

        Two-step pipeline when modelo_referencia_url is present:
          1. IP-Adapter FaceID → model with consistent face
          2. image-to-image  → apply jewelry to each generated model image

        Fallback (no reference): single image-to-image pass.
        """
        modelo_url = payload.get("modelo_referencia_url", "")

        if modelo_url:
            return self._pipeline_with_face(payload, modelo_url)

        return fal_client.generate_images(
            prompt=payload.get("prompt", ""),
            image_base64=payload.get("image_base64", ""),
            num_images=payload.get("num_images", 2),
        )

    def _pipeline_with_face(self, payload: Dict[str, Any], modelo_url: str) -> Dict[str, Any]:
        """Two-step generation: face consistency + jewelry application."""
        prompt = payload.get("prompt", "")
        jewelry_base64 = payload.get("image_base64", "")
        num_images = payload.get("num_images", 2)

        logger.info("Pipeline 2 etapas: IP-Adapter FaceID → apply_jewelry")

        # Step 1: gera modelo com rosto consistente
        step1 = fal_client.generate_model_with_face(
            face_image_url=modelo_url,
            prompt=prompt,
            num_images=num_images,
        )
        if not step1.get("success"):
            return step1

        # Step 2: aplica a joia em cada imagem gerada
        final_images: List[Dict[str, Any]] = []
        for img in step1["images"]:
            step2 = fal_client.apply_jewelry(
                model_image_url=img["url"],
                jewelry_base64=jewelry_base64,
                prompt=prompt,
            )
            if step2.get("success"):
                final_images.extend(step2["images"])
            else:
                # fallback: usa a imagem sem a joia aplicada
                logger.warning(f"apply_jewelry falhou para {img['url']}, usando imagem do step1")
                final_images.append(img)

        return {"success": True, "images": final_images}

    def generate_video(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Generates animated video via Kling (through Fal.ai)."""
        return video_client.generate_video(
            image_url=payload.get("image_url", ""),
            prompt=payload.get("prompt", ""),
        )


n8n_client = AIPipeline()
