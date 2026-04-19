"""
GlowStudio AI - Maritaca AI Client
Direct API integration for text generation (replaces N8N text workflow).
"""

import json
import time
import requests
from typing import Dict, Any, List
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

_API_URL = "https://chat.maritaca.ai/api/chat/completions"

_SYSTEM_PROMPT = (
    "Você é um copywriter especializado em semijoias brasileiras de luxo acessível. "
    "Crie legendas persuasivas, sofisticadas e com alto poder de conversão para redes sociais. "
    "Inclua emojis relevantes, hashtags estratégicas e um CTA claro. "
    "Responda APENAS em JSON válido com os campos \"legenda\" e \"prompt_visual\"."
)

_OBJETIVO_TONE = {
    "Venda Direta": "foco em conversão imediata, urgência e benefícios da peça",
    "Autoridade": "foco em expertise, qualidade artesanal e tradição",
    "Lifestyle": "foco em estilo de vida, aspiração e identidade da marca",
    "Educativo": "foco em informações sobre o material, cuidados e diferenciais técnicos",
}

_PUBLICO_STYLE = {
    "Noivas": "elegante e emocionante, voltado para o grande dia e momentos especiais",
    "Executivas": "sofisticado e profissional, poder e refinamento no dia a dia",
    "Minimalistas": "clean, essencial, beleza na simplicidade",
    "Presente": "emotivo e afetivo, ideal para presentear quem você ama",
}


def _build_user_prompt(objetivo: str, publico: str, diferenciais: List[str]) -> str:
    diferenciais_str = ", ".join(diferenciais) if diferenciais else "alta qualidade artesanal"
    tone = _OBJETIVO_TONE.get(objetivo, objetivo)
    style = _PUBLICO_STYLE.get(publico, publico)

    return f"""Crie conteúdo para uma semijoia com as seguintes características:
- Objetivo: {objetivo} ({tone})
- Público-alvo: {publico} ({style})
- Diferenciais: {diferenciais_str}

Retorne JSON com:
1. "legenda": texto persuasivo para Instagram/WhatsApp (máx 300 caracteres + hashtags)
2. "prompt_visual": prompt em inglês para Fal.ai (modelo fotorrealista vestindo a joia)

Formato do prompt_visual:
"[descrição da modelo: etnia, idade, expressão, cabelo] wearing [descrição da joia], [cenário], [iluminação de estúdio], photorealistic, 8k, commercial photography"
"""


class MaritacaClient:
    def __init__(self):
        self.api_key = settings.MARITACA_API_KEY
        self.model = settings.MARITACA_MODEL
        self.timeout = 30

    def generate_content(self, objetivo: str, publico: str, diferenciais: List[str]) -> Dict[str, Any]:
        if not self.api_key:
            return self._mock(objetivo, publico, diferenciais)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Key {self.api_key}",
        }
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": _build_user_prompt(objetivo, publico, diferenciais)},
            ],
            "temperature": 0.8,
            "max_tokens": 600,
        }

        try:
            logger.info(f"Maritaca AI: gerando conteúdo — modelo={self.model}")
            resp = requests.post(_API_URL, json=body, headers=headers, timeout=self.timeout)
            resp.raise_for_status()

            raw = resp.json()["choices"][0]["message"]["content"].strip()
            raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            data = json.loads(raw)

            if "legenda" not in data or "prompt_visual" not in data:
                return {"success": False, "error": "Resposta da Maritaca AI incompleta."}

            return {"success": True, "legenda": data["legenda"], "prompt_visual": data["prompt_visual"]}

        except requests.exceptions.Timeout:
            logger.error("Timeout na Maritaca AI")
            return {"success": False, "error": "Maritaca AI demorou demais para responder (timeout)."}
        except json.JSONDecodeError as e:
            logger.error(f"JSON inválido da Maritaca AI: {e}")
            return {"success": False, "error": "Resposta inesperada da Maritaca AI. Tente novamente."}
        except Exception as e:
            logger.error(f"Erro na Maritaca AI: {e}")
            return {"success": False, "error": str(e)}

    def _mock(self, objetivo: str, publico: str, diferenciais: List[str]) -> Dict[str, Any]:
        logger.info("Maritaca AI: modo mock ativo (MARITACA_API_KEY não configurada)")
        time.sleep(1)
        dif = ", ".join(diferenciais) if diferenciais else "alta qualidade"
        return {
            "success": True,
            "legenda": (
                f"✨ Sofisticação que fala por você ✨\n\n"
                f"Para {publico.lower()}: semijoia com {dif}.\n"
                f"✅ {objetivo} — elegância acessível.\n\n"
                f"#Semijoias #LuxoAcessivel #GlowStudioAI"
            ),
            "prompt_visual": (
                "Elegant Brazilian woman, 28 years old, natural makeup, dark hair, "
                "wearing a delicate 18k gold-plated semijoia necklace, white studio background, "
                "professional soft-box lighting, photorealistic, 8k, commercial jewelry photography"
            ),
        }


maritaca_client = MaritacaClient()
