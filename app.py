"""
============================================
GlowStudio AI - Navigation Manager (Root)
============================================
Orquestrador central de navegação e identidade visual.
Rodando da raiz para compatibilidade total com Docker.
"""

import sys
import os
from pathlib import Path

# Garante que a pasta src seja vista como módulo
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st
from src.config.settings import settings
from src.config.theme import inject_custom_css
from src.services.session_manager import init_session_state
from src.services.supabase_client import check_session
from src.utils.logger import get_logger
from src.components import render_sidebar_logo, render_sidebar_info, render_sidebar_menu

logger = get_logger(__name__)

# --- Configuração Global ---
st.set_page_config(
    page_title=settings.APP_NAME,
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Inicialização ---
init_session_state()
inject_custom_css()
check_session()

is_auth = st.session_state.get("is_authenticated", False)

# --- Definição de Páginas (Caminhos da Raiz) ---
pub_pages = [
    st.Page("src/views/home.py", title="Início", icon="💎", default=True),
]

if is_auth:
    auth_pages = [
        st.Page("src/views/01_configuracao.py", title="Configuração", icon="⚙️"),
        st.Page("src/views/02_edicao.py", title="Curadoria", icon="✍️"),
        st.Page("src/views/03_estudio.py", title="Estúdio Criativo", icon="🎨"),
        st.Page("src/views/04_historico.py", title="Histórico de Joias", icon="📜"),
    ]
else:
    auth_pages = [
        st.Page("src/views/login.py", title="Acesso Exclusivo", icon="🔑"),
    ]

# --- Execução da Navegação ---
pages = pub_pages + auth_pages
# Usamos position="hidden" para construir nosso próprio menu na sidebar (Garante a Ordem)
pg = st.navigation(pages, position="hidden")

# --- Renderização da Sidebar (Ordem Garantida) ---
with st.sidebar:
    render_sidebar_logo()
    render_sidebar_menu(pages)
    render_sidebar_info()
    
    if is_auth and st.session_state.get("user_email"):
        st.markdown(f"<div style='padding: 0 10px; margin-bottom: 10px; font-size: 0.85rem; color: #1A1A1A;'>👤 {st.session_state['user_email']}</div>", unsafe_allow_html=True)
        if st.button("🚪 Encerrar Sessão", key="btnLogoutSidebar", use_container_width=True):
            from src.services.supabase_client import sign_out
            sign_out()
            st.rerun()

    if settings.is_development:
        st.markdown("<div style='margin-top: auto; padding: 20px 10px;'>", unsafe_allow_html=True)
        st.caption(f"🔧 v1.0 • {settings.APP_ENV}")
        st.markdown("</div>", unsafe_allow_html=True)

# --- Execução da Página Principal ---
try:
    pg.run()
except Exception as e:
    st.error(f"Erro ao carregar página: {e}")
    logger.error(f"Erro na navegação: {e}")
