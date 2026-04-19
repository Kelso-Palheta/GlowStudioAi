"""
GlowStudio AI - AI Pipeline
Orchestrates direct calls to Maritaca AI, Fal.ai, and Kling.
Replaces the N8N middleware layer. Public interface is unchanged.
"""

from typing import Dict, Any
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
        )

    def generate_images(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Generates product images via Fal.ai (image-to-image inpainting)."""
        return fal_client.generate_images(
            prompt=payload.get("prompt", ""),
            image_base64=payload.get("image_base64", ""),
            num_images=payload.get("num_images", 2),
        )

    def generate_video(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Generates animated video via Kling (through Fal.ai)."""
        return video_client.generate_video(
            image_url=payload.get("image_url", ""),
            prompt=payload.get("prompt", ""),
        )


n8n_client = AIPipeline()
