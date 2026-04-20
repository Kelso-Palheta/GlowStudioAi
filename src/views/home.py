import streamlit as st
from src.components import render_sidebar_branding, render_progress_header

def render_home():
    """Renderiza a Landing Page / Showroom do GlowStudio AI."""
    
    # Hero Section
    st.markdown(
        """
        <div class="hero-section">
            <h1 class="hero-title">
                Glow<span class="hero-highlight">Studio</span> AI
            </h1>
            <p class="hero-subtitle">
                A tecnologia que veste suas semijoias em modelos reais.<br>
                Visual fotorrealista • Legendas persuasivas • Vídeos de alto impacto
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Cards de Features
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">💎</div>
                <h3 class="feature-title">Estratégia de Luxo</h3>
                <p class="feature-desc">
                    Defina o público e o objetivo. Nossa IA entende o mercado de semijoias.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">✨</div>
                <h3 class="feature-title">Modelos Virtuais</h3>
                <p class="feature-desc">
                    Sua peça vestida por modelos fotorrealistas em cenários de alto padrão.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">👑</div>
                <h3 class="feature-title">Vídeos de Grife</h3>
                <p class="feature-desc">
                    Animações cinematográficas prontas para Reels e Stories do Instagram.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Botão de Ação
    st.markdown("<br>", unsafe_allow_html=True)
    col_spacer1, col_btn, col_spacer2 = st.columns([1, 2, 1])
    with col_btn:
        if st.button("✨ Começar Agora", type="primary", use_container_width=True):
            if st.session_state.get("is_authenticated"):
                st.switch_page("views/01_configuracao.py")
            else:
                st.switch_page("views/login.py")

    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="footer">
            <p>💎 GlowStudio AI — Transformando semijoias em conteúdo premium</p>
            <p class="footer-sub">Abril 2026 • Versão 1.0</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    render_home()
