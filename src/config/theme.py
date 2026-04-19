"""
============================================
GlowStudio AI - Theme & Design Tokens
============================================
Identidade visual: Safety Blue + Prata/Dourado em Dark Mode.
Referência: Documento Mestre, Seção 12 (Identidade Visual).
"""

import streamlit as st
from pathlib import Path


class _Theme:
    """Design tokens centralizados (Luxury Boutique Edition)."""

    # --- Cores Primárias (Dourado de Luxo) ---
    PRIMARY = "#D4AF37"
    PRIMARY_DARK = "#B08D26"
    PRIMARY_LIGHT = "#F2E3B6"

    # --- Acentos ---
    ACCENT_GOLD = "#D4AF37"
    ACCENT_CHAMPAGNE = "#F5E6D3" # Novo Champagne
    ACCENT_SILVER = "#E0E0E0"

    # --- Background ---
    BG_DARK = "#FDFBF9"
    BG_CARD = "#FFFFFF"
    BG_CARD_HOVER = "#FCF9F5"
    BG_INPUT = "#FFFFFF"

    # --- Texto ---
    TEXT_PRIMARY = "#1A1A1A"
    TEXT_SECONDARY = "#4A4A4A"
    TEXT_MUTED = "#8E8E8E"

    # --- Feedback ---
    SUCCESS = "#27AE60"
    ERROR = "#C0392B"
    WARNING = "#D35400"
    INFO = "#3498DB"

    # --- Tipografia ---
    FONT_HEADING = "'Playfair Display', serif" # Nova fonte principal
    FONT_BODY = "'Inter', system-ui, -apple-system, sans-serif"
    FONT_CODE = "'JetBrains Mono', 'Fira Code', monospace"

    # --- Espaçamento ---
    RADIUS_SM = "4px" # Mais angular e sofisticado
    RADIUS_MD = "8px"
    RADIUS_LG = "12px"
    RADIUS_XL = "0px" # Bordas retas são mais luxuosas em certos contextos

    # --- Gradientes ---
    GRADIENT_PRIMARY = f"linear-gradient(135deg, {PRIMARY} 0%, {PRIMARY_DARK} 100%)"
    GRADIENT_GOLD = f"linear-gradient(135deg, {ACCENT_GOLD} 0%, #B8942E 100%)"
    GRADIENT_CHAMPAGNE = f"linear-gradient(180deg, {BG_CARD} 0%, {ACCENT_CHAMPAGNE} 100%)"




# Singleton
theme = _Theme()


def inject_custom_css():
    """Injeta CSS customizado no Streamlit via st.markdown.
    
    Carrega o arquivo assets/css/style.css e aplica como estilo global.
    Deve ser chamado uma vez no início do app (app.py).
    """
    css_path = Path(__file__).resolve().parent.parent.parent / "assets" / "css" / "style.css"

    if css_path.exists():
        css_content = css_path.read_text(encoding="utf-8")
        # st.html was isolating the styles in this Streamlit version. We MUST use markdown.
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        # CSS inline de fallback caso o arquivo não exista
        st.markdown(
            f"""
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
                
                html, body, [class*="css"] {{
                    font-family: {theme.FONT_BODY};
                }}
                
                h1, h2, h3, h4 {{
                    font-family: {theme.FONT_HEADING};
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )
