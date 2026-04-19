"""
============================================
GlowStudio AI - Tela 1: Configuração Estratégica
============================================
Upload da semijoia + seleção de estratégia de marketing.
Referência: Documento Mestre, Seção 6.3 — Tela 1.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
from src.config.theme import inject_custom_css
from src.services.session_manager import init_session_state, set_etapa, has_uploaded_image
from src.services.image_processor import resize_image, to_base64
from src.utils.validators import validate_image
from src.utils.logger import get_logger

logger = get_logger(__name__)

# --- Inicialização ---
init_session_state()

from src.components import render_progress_header

# --- Configuração da Página ---
render_progress_header(current_step=1)

st.markdown(
    """
    <div class="page-header" style="padding-top: 0;">
        <h1 class="page-title">📸 Configuração Estratégica</h1>
        <p class="page-subtitle">Envie a foto da sua semijoia e defina a estratégia de marketing</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# --- Layout em duas colunas ---
col_upload, col_config = st.columns([1, 1], gap="large")

# === Coluna Esquerda: Upload ===
with col_upload:
    st.markdown("### 💎 Foto da Semijoia")

    uploaded_file = st.file_uploader(
        "Arraste ou selecione a foto da sua peça",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=False,
        key="file_uploader",
        help="Formatos aceitos: PNG, JPG, WEBP. Tamanho máximo: 10MB.",
    )

    if uploaded_file is not None:
        # Validar imagem
        result = validate_image(uploaded_file)

        if result.is_valid:
            # Armazenar no session_state
            st.session_state["uploaded_image"] = uploaded_file.getvalue()
            st.session_state["uploaded_filename"] = uploaded_file.name

            # Preview
            st.image(
                uploaded_file,
                caption=f"📷 {uploaded_file.name}",
                use_container_width=True,
            )
            st.success("✅ Imagem carregada com sucesso!")
            logger.info(f"Imagem carregada: {uploaded_file.name} ({uploaded_file.size} bytes)")
        else:
            st.error(f"❌ {result.error_message}")
            logger.warning(f"Upload rejeitado: {result.error_message}")

    elif has_uploaded_image():
        # Mostrar preview da imagem já carregada na sessão
        st.image(
            st.session_state["uploaded_image"],
            caption=f"📷 {st.session_state['uploaded_filename']}",
            use_container_width=True,
        )
        st.info("ℹ️ Imagem já carregada. Faça novo upload para substituir.")

# === Coluna Direita: Configuração ===
with col_config:
    st.markdown("### 🎯 Estratégia de Marketing")

    # Objetivo de Marketing
    objetivo = st.selectbox(
        "Objetivo da Publicação",
        options=["", "Venda Direta", "Autoridade", "Lifestyle", "Educativo"],
        index=0,
        key="select_objetivo",
        help="Qual o objetivo principal desta publicação?",
    )
    if objetivo:
        st.session_state["objetivo"] = objetivo

    # Público-Alvo
    publico = st.selectbox(
        "Público-Alvo",
        options=["", "Noivas", "Executivas", "Minimalistas", "Presente"],
        index=0,
        key="select_publico",
        help="Para qual perfil de cliente esta peça é ideal?",
    )
    if publico:
        st.session_state["publico"] = publico

    # Diferenciais
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ✅ Diferenciais da Peça")

    diferenciais = st.multiselect(
        "Selecione os diferenciais",
        options=["Banho 18k", "Ródio", "Hipoalergênico", "Nanotecnologia"],
        default=st.session_state.get("diferenciais", []),
        key="select_diferenciais",
        help="Marque todos os diferenciais que se aplicam.",
    )
    st.session_state["diferenciais"] = diferenciais

# --- Resumo da Configuração ---
st.markdown("---")

if has_uploaded_image() and st.session_state.get("objetivo") and st.session_state.get("publico"):
    st.markdown(
        f"""
        <div class="config-summary">
            <h3>📋 Resumo da Configuração</h3>
            <div class="summary-grid">
                <div class="summary-item">
                    <span class="summary-label">📷 Imagem</span>
                    <span class="summary-value">{st.session_state['uploaded_filename']}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">🎯 Objetivo</span>
                    <span class="summary-value">{st.session_state['objetivo']}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">👥 Público</span>
                    <span class="summary-value">{st.session_state['publico']}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">✅ Diferenciais</span>
                    <span class="summary-value">{', '.join(st.session_state['diferenciais']) or 'Nenhum selecionado'}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Botão para avançar
    col_s1, col_btn, col_s2 = st.columns([1, 2, 1])
    with col_btn:
        if st.button(
            "✨  Gerar Conteúdo",
            type="primary",
            use_container_width=True,
            key="btn_generate",
        ):
            with st.status("💎 Orquestrando sua Curadoria de Luxo...", expanded=True) as status:
                st.write("💍 Analisando Estilo da Joia...")
                # Skill 4: Processamento de imagem
                img_bytes = st.session_state["uploaded_image"]
                processed_bytes = resize_image(img_bytes)
                
                st.write("✍️ Redigindo Legenda Persuasiva...")
                # Skill 2: Preparação Base64
                img_base64 = to_base64(processed_bytes)
                
                st.write("🎨 Preparando Estúdio de IA...")
                # Salvar no session_state para as próximas telas
                st.session_state["uploaded_image_processed"] = processed_bytes
                st.session_state["uploaded_image_base64"] = img_base64
                
                # Resetar textos da etapa 2 se for uma nova imagem/config
                st.session_state["legenda_gerada"] = ""
                st.session_state["prompt_visual"] = ""
                st.session_state["texto_aprovado"] = False
                st.session_state["imagens_geradas"] = []
                
                status.update(label="✅ Curadoria Preparada!", state="complete", expanded=False)

            set_etapa(2)
            logger.info(
                f"Imagem processada e avançando para Etapa 2. "
                f"Objetivo: {st.session_state['objetivo']}"
            )
            st.switch_page("src/views/02_edicao.py")

else:
    # Checklist do que falta
    st.markdown(
        """
        <div class="config-checklist">
            <h3>📝 Complete todos os campos para continuar:</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    items = [
        ("📷 Upload da imagem", has_uploaded_image()),
        ("🎯 Objetivo de marketing", bool(st.session_state.get("objetivo"))),
        ("👥 Público-alvo", bool(st.session_state.get("publico"))),
    ]

    for label, done in items:
        icon = "✅" if done else "⬜"
        st.markdown(f"{icon} {label}")
