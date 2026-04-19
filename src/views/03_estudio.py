"""
============================================
GlowStudio AI - Tela 3: Estúdio de Resultados
============================================
Galeria de imagens, download e animação de vídeo.
Referência: Documento Mestre, Seção 6.3 — Tela 3.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
from src.config.theme import inject_custom_css
from src.services.session_manager import (
    init_session_state,
    set_etapa,
    has_uploaded_image,
    reset_session,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)

# --- Inicialização ---
init_session_state()

from src.components import render_progress_header

# --- Header ---
render_progress_header(current_step=3)

# --- Guard: verificar se há dados gerados ---
if not st.session_state.get("texto_aprovado"):
    st.markdown(
        """
        <div class="page-header" style="padding-top: 0;">
            <h1 class="page-title">🎨 Estúdio Criativo</h1>
            <p class="page-subtitle">Gere os visuais finais e animações para sua semijoia</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.warning("⚠️ Nenhuma criação encontrada. Por favor, aprove as sugestões na etapa de Curadoria primeiro.")
    if st.button("← Ir para Curadoria", key="btn_back_to_t2"):
        st.switch_page("src/views/02_edicao.py")
    st.stop()

st.markdown(
    """
    <div class="page-header" style="padding-top: 0;">
        <h1 class="page-title">🎨 Estúdio de Resultados</h1>
        <p class="page-subtitle">Suas imagens geradas e conteúdo pronto para publicação</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# --- Status de Geração ---
# --- Geração automática de imagens (Skill 1 + 2) ---
if not st.session_state.get("imagens_geradas"):
    with st.status("🎨 Criando Visuais Exclusivos...", expanded=True) as status:
        from src.services.n8n_client import n8n_client
        
        modelo_url = st.session_state.get("modelo_referencia_url", "")
        if modelo_url:
            st.write("👤 Aplicando rosto da sua modelo de referência...")
        else:
            st.write("👗 Selecionando os melhores modelos de IA...")
        payload = {
            "prompt": st.session_state.get("prompt_visual", ""),
            "image_base64": st.session_state.get("uploaded_image_base64", ""),
            "modelo_referencia_url": modelo_url,
            "objetivo": st.session_state.get("objetivo", ""),
            "publico": st.session_state.get("publico", ""),
        }
        
        st.write("✨ Vestindo a modelo com sua joia...")
        result = n8n_client.generate_images(payload)
        
        if result.get("success"):
            st.write("💎 Finalizando texturas e iluminação...")
            imgs = result.get("images", [])
            st.session_state["imagens_geradas"] = imgs
            
            # --- Persistência (Fase 3) ---
            from src.services.supabase_client import save_generation
            for img in imgs:
                save_generation(
                    gen_type="image",
                    image_url=img.get("url"),
                    caption=st.session_state.get("legenda_gerada"),
                    prompt=st.session_state.get("prompt_visual"),
                    marketing_objective=st.session_state.get("objetivo"),
                    target_audience=st.session_state.get("publico"),
                    features=st.session_state.get("diferenciais", [])
                )
            status.update(label="✅ Galeria de Luxo Criada!", state="complete", expanded=False)
            st.rerun()
        else:
            status.update(label="❌ Erro na Geração", state="error", expanded=True)
            st.error(f"Detalhes: {result.get('error')}")
            if st.button("🔄 Tentar Novamente", key="btn_retry_images"):
                st.rerun()

imagens = st.session_state.get("imagens_geradas", [])

if not imagens:
    # Este bloco raramente será visto devido ao st.rerun acima
    st.info("🔜 Aguardando geração de imagens...")

    # Mostrar a imagem original como referência
    st.markdown("### 📷 Imagem Original (referência)")
    col_img, col_info = st.columns([1, 1])
    with col_img:
        if has_uploaded_image():
            st.image(
                st.session_state["uploaded_image"],
                caption=st.session_state["uploaded_filename"],
                use_container_width=True,
            )
    with col_info:
        st.markdown(
            f"""
            <div class="config-summary compact">
                <h4>Configuração usada:</h4>
                <p><strong>🎯 Objetivo:</strong> {st.session_state.get('objetivo', '—')}</p>
                <p><strong>👥 Público:</strong> {st.session_state.get('publico', '—')}</p>
                <p><strong>✅ Diferenciais:</strong> {', '.join(st.session_state.get('diferenciais', [])) or '—'}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

else:
    # Galeria de imagens geradas
    st.markdown("### 🖼️ Galeria de Imagens Geradas")

    # Galeria dinâmica via Componente (Skill 1)
    from src.components import render_gallery
    
    def on_animar_click(idx: int, img_data: dict):
        with st.status("🎬 Transformando em Obra de Arte Móvel...", expanded=True) as status:
            from src.services.n8n_client import n8n_client
            
            st.write("🎞️ Capturando fluidez e movimento...")
            video_payload = {
                "image_url": img_data.get("url", ""),
                "image_base64": st.session_state.get("uploaded_image_base64", ""),
                "prompt": st.session_state.get("prompt_visual", ""),
            }
            
            st.write("🎥 Renderizando vídeo em qualidade Cinema...")
            video_result = n8n_client.generate_video(video_payload)
            
            if video_result.get("success"):
                video_url = video_result.get("video_url")
                if video_url:
                    st.write("✨ Finalização Luxo concluída!")
                    st.session_state["video_gerado"] = video_url
                    
                    # --- Persistência (Fase 3) ---
                    from src.services.supabase_client import save_generation
                    save_generation(
                        gen_type="video",
                        image_url=video_url,
                        caption=st.session_state.get("legenda_gerada"),
                        prompt=st.session_state.get("prompt_visual"),
                        marketing_objective=st.session_state.get("objetivo"),
                        target_audience=st.session_state.get("publico"),
                        features=st.session_state.get("diferenciais", [])
                    )
                    status.update(label="✅ Vídeo Pronto para Download!", state="complete", expanded=False)
                    st.rerun()
                else:
                    status.update(label="⏳ Simulação Concluída", state="complete", expanded=True)
                    st.info(video_result.get("message", "Vídeo mock — conecte o webhook para ativar."))
            else:
                status.update(label="❌ Falha na Animação", state="error", expanded=True)
                st.error(f"Detalhes: {video_result.get('error')}")

    render_gallery(
        images=imagens,
        columns=2,
        show_download=True,
        show_action=True,
        action_label="🎬 Animar",
        action_callback=on_animar_click,
        action_disabled=False
    )

# --- Legenda Final ---
st.markdown("---")
st.markdown("### 📋 Legenda para Redes Sociais")
st.caption("Copie e cole diretamente no Instagram, WhatsApp ou Facebook")

legenda_final = st.session_state.get("legenda_gerada", "")
st.code(legenda_final, language=None)

if legenda_final:
    st.download_button(
        "📥 Baixar Legenda (.txt)",
        data=legenda_final,
        file_name="glowstudio_legenda.txt",
        mime="text/plain",
        key="dl_legenda",
    )

# --- Vídeo Gerado ---
video = st.session_state.get("video_gerado")
if video:
    st.markdown("---")
    st.markdown("### 🎬 Vídeo Animado")
    st.video(video)
    st.download_button(
        "📥 Baixar Vídeo (MP4)",
        data=video,
        file_name="glowstudio_video.mp4",
        mime="video/mp4",
        key="dl_video",
    )

# --- Botões de Ação ---
st.markdown("---")

col_back, col_spacer, col_new = st.columns([1, 2, 1])

with col_back:
    if st.button("← Voltar para Edição", key="btn_back", use_container_width=True):
        st.switch_page("src/views/02_edicao.py")

with col_new:
    if st.button(
        "🔄 Nova Geração",
        type="primary",
        use_container_width=True,
        key="btn_new",
    ):
        reset_session()
        logger.info("Sessão resetada — nova geração iniciada")
        st.switch_page("src/views/01_configuracao.py")
