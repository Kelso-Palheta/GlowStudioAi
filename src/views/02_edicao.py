"""
============================================
GlowStudio AI - Tela 2: Edição e Aprovação
============================================
Edição dos textos gerados pela Maritaca AI.
Referência: Documento Mestre, Seção 6.3 — Tela 2.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
from src.config.settings import settings
from src.config.theme import inject_custom_css
from src.services.session_manager import (
    init_session_state,
    set_etapa,
    has_uploaded_image,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)

# --- Validação de Configuração (Skill 5) ---
config_errors = settings.validate()
if config_errors and settings.is_production:
    st.error("🚨 Erros de configuração detectados:")
    for err in config_errors:
        st.write(f"- {err}")
    st.stop()

# --- Inicialização ---
init_session_state()

from src.components import render_progress_header

# --- Header ---
render_progress_header(current_step=2)

# --- Guard: verificar se há dados da Tela 1 ---
if not has_uploaded_image():
    st.markdown(
        """
        <div class="page-header" style="padding-top: 0;">
            <h1 class="page-title">✍️ Edição e Aprovação</h1>
            <p class="page-subtitle">Revise e edite os textos gerados pela IA antes de gerar a imagem</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.warning("⚠️ Nenhuma imagem carregada. Por favor, realize o upload no Showroom primeiro.")
    if st.button("← Ir para Upload", key="btn_back_to_t1"):
        st.switch_page("src/views/01_configuracao.py")
    st.stop()

st.markdown(
    """
    <div class="page-header" style="padding-top: 0;">
        <h1 class="page-title">✍️ Edição e Aprovação</h1>
        <p class="page-subtitle">Revise e edite os textos gerados pela IA antes de gerar a imagem</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# --- Layout em duas colunas ---
col_text, col_preview = st.columns([3, 2], gap="large")

# === Coluna Esquerda: Edição de Textos ===
with col_text:
    # Legenda de Vendas
    st.markdown("### 📝 Legenda de Vendas")
    st.caption("Gerada pela Maritaca AI — edite livremente")

    # Geração automática caso não exista (Skill 1 + 2)
    if not st.session_state.get("legenda_gerada"):
        with st.spinner("🧠 Maritaca AI desenhando sua estratégia..."):
            payload = {
                "objetivo": st.session_state["objetivo"],
                "publico": st.session_state["publico"],
                "diferenciais": st.session_state["diferenciais"],
                "image_base64": st.session_state.get("uploaded_image_base64", "")
            }
            from src.services.n8n_client import n8n_client
            result = n8n_client.generate_content(payload)
            
            if result.get("success"):
                st.session_state["legenda_gerada"] = result["legenda"]
                st.session_state["prompt_visual"] = result["prompt_visual"]
                st.rerun()
            else:
                st.error(f"❌ Erro ao gerar textos: {result.get('error')}")
                
                # Melhoria no botão de retentativa: usamos um container para controle visual
                if st.button("🔄 Tentar Novamente", key="btn_retry_text", type="primary"):
                    # Forçamos a limpeza de estados que possam estar travando a geração
                    st.session_state["legenda_gerada"] = ""
                    st.session_state["prompt_visual"] = ""
                    st.rerun()
                
                st.info("💡 Dica: Verifique se MARITACA_API_KEY está configurada corretamente no arquivo .env.")
                st.stop()

    legenda = st.text_area(
        "Legenda",
        value=st.session_state.get("legenda_gerada", ""),
        height=200,
        key="input_legenda",
        label_visibility="collapsed",
        placeholder="A legenda de vendas aparecerá aqui após a geração...",
    )
    st.session_state["legenda_gerada"] = legenda

    st.markdown("<br>", unsafe_allow_html=True)

    # Prompt Visual
    st.markdown("### 🎨 Prompt Visual (para geração da modelo)")
    st.caption("Este prompt será enviado ao Fal.ai para criar a modelo com sua joia")

    prompt = st.text_area(
        "Prompt Visual",
        value=st.session_state.get("prompt_visual", ""),
        height=150,
        key="input_prompt",
        label_visibility="collapsed",
        placeholder="O prompt visual aparecerá aqui após a geração...",
    )
    st.session_state["prompt_visual"] = prompt

    # Botão para regenerar texto (Skill 3: Copywriting)
    if st.button("🔄 Regenerar Textos", key="btn_regenerate"):
        st.session_state["legenda_gerada"] = ""
        st.session_state["prompt_visual"] = ""
        st.rerun()

# === Coluna Direita: Preview da Imagem ===
with col_preview:
    st.markdown("### 📷 Imagem Original")

    if has_uploaded_image():
        st.image(
            st.session_state["uploaded_image"],
            caption=st.session_state["uploaded_filename"],
            use_container_width=True,
        )

    # Resumo da configuração da Tela 1
    st.markdown(
        f"""
        <div class="config-summary compact">
            <p><strong>🎯 Objetivo:</strong> {st.session_state.get('objetivo', '—')}</p>
            <p><strong>👥 Público:</strong> {st.session_state.get('publico', '—')}</p>
            <p><strong>✅ Diferenciais:</strong> {', '.join(st.session_state.get('diferenciais', [])) or '—'}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Botões de Navegação ---
st.markdown("---")

col_back, col_spacer, col_next = st.columns([1, 2, 1])

with col_back:
    if st.button("← Voltar", key="btn_back", use_container_width=True):
        st.switch_page("src/views/01_configuracao.py")

with col_next:
    if st.button(
        "✨ Aprovar e Gerar Imagem →",
        type="primary",
        use_container_width=True,
        key="btn_approve",
    ):
        st.session_state["texto_aprovado"] = True
        set_etapa(3)
        logger.info("Texto aprovado pelo usuário, avançando para geração de imagem")
        st.switch_page("src/views/03_estudio.py")
