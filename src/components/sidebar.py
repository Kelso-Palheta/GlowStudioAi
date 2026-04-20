import streamlit as st

def render_sidebar_logo():
    """Renderiza apenas o logo no topo da sidebar."""
    st.markdown(
        """
        <div class="sidebar-brand">
            <span class="brand-icon">💎</span>
            <span class="brand-text">GlowStudio AI</span>
            <span class="brand-tagline">A Arte da Joalheria com IA</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar_menu(pages):
    """Renderiza menu de navegação na sidebar respeitando a ordem do orquestrador."""
    for page in pages:
        st.page_link(page)

def render_sidebar_info():
    """Renderiza os cards de status e missão."""
    st.markdown(
        """
        <div class="sidebar-info-card" style="padding-top: 10px;">
            <p style="font-size: 0.75rem; color: #8E8E8E; margin-bottom: 5px; letter-spacing: 0.1em; font-weight: 700;">STATUS DA CONTA</p>
            <p style="font-size: 0.9rem; font-weight: 700; color: #D4AF37;">MEMBRO PREMIUM</p>
            <div style="height: 1px; width: 100%; background: rgba(212, 175, 55, 0.1); margin-top: 5px;"></div>
        </div>
        <div class="sidebar-mission">
            <p style="margin-top: 15px; font-size: 0.85rem; color: #4A4A4A; line-height: 1.4; padding: 0 10px;">
                Curadoria de excelência visual para o mercado de alta joalheria brasileira.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar_branding():
    """Mantido para retrocompatibilidade."""
    render_sidebar_logo()
    render_sidebar_info()
