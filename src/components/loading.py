"""
============================================
GlowStudio AI - Loading Component
============================================
Skill 1: UI/UX Streamlit (Frontend)

Animações de carregamento premium com
skeleton placeholders e mensagens contextuais.
"""

import streamlit as st
from typing import Optional


def render_skeleton_loader(message: str = "Processando...", icon: str = "💎"):
    """
    Renderiza um skeleton loader premium com shimmer animation.

    Args:
        message: Mensagem exibida durante o carregamento
        icon: Emoji ícone para contexto visual
    """
    st.markdown(
        f"""
        <div class="skeleton-container">
            <div class="skeleton-icon">{icon}</div>
            <div class="skeleton-text">{message}</div>
            <div class="skeleton-bar">
                <div class="skeleton-bar-fill"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_success_animation(message: str = "Concluído com sucesso!"):
    """
    Renderiza uma animação de sucesso (checkmark + confetti).

    Args:
        message: Mensagem de sucesso
    """
    st.markdown(
        f"""
        <div class="success-container">
            <div class="success-checkmark">
                <div class="check-icon">
                    <span class="icon-line line-tip"></span>
                    <span class="icon-line line-long"></span>
                    <div class="icon-circle"></div>
                    <div class="icon-fix"></div>
                </div>
            </div>
            <p class="success-message">{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Mensagens contextuais para cada fase do pipeline
LOADING_MESSAGES = {
    "text": {
        "message": "🧠 Maritaca AI preparando sua estratégia de vendas...",
        "icon": "🧠",
    },
    "image": {
        "message": "🎨 Fal.ai vestindo a modelo com sua joia...",
        "icon": "🎨",
    },
    "video": {
        "message": "🎬 Animando sua modelo para vídeo de divulgação...",
        "icon": "🎬",
    },
    "processing": {
        "message": "💎 Processando sua semijoia...",
        "icon": "💎",
    },
}


def get_loading_context(phase: str) -> dict:
    """
    Retorna a mensagem e ícone corretos para cada fase do pipeline.

    Args:
        phase: 'text', 'image', 'video' ou 'processing'

    Returns:
        Dict com 'message' e 'icon'
    """
    return LOADING_MESSAGES.get(phase, LOADING_MESSAGES["processing"])
