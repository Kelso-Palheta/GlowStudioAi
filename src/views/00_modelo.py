"""
GlowStudio AI - Etapa 0: Minhas Modelos
Gerenciamento de múltiplas modelos virtuais de referência por marca.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
from src.config.theme import inject_custom_css
from src.services.session_manager import (
    init_session_state,
    load_modelos_from_supabase,
    get_modelos,
    get_modelo_ativa,
    set_modelo_ativa,
    add_modelo_referencia,
    remove_modelo_referencia,
    has_modelo_referencia,
)
from src.services.image_processor import resize_image, to_base64
from src.utils.validators import validate_image
from src.utils.logger import get_logger

logger = get_logger(__name__)

init_session_state()
inject_custom_css()

# Carrega modelos do Supabase (executa apenas uma vez por sessão)
load_modelos_from_supabase()

st.markdown(
    """
    <div class="page-header" style="padding-top: 0;">
        <h1 class="page-title">👤 Minhas Modelos</h1>
        <p class="page-subtitle">Gerencie as identidades visuais da sua marca — selecione qual modelo usar em cada criação</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

modelos = get_modelos()
modelo_ativa = get_modelo_ativa()

# ─── Galeria de Modelos Existentes ───────────────────────────────────────────

if modelos:
    ativa_id = st.session_state.get("modelo_ativa_id")
    qtd = len(modelos)
    st.markdown(f"### 🗂️ Suas Modelos ({qtd})")
    st.caption("Clique em **Usar agora** para selecionar a modelo ativa para as próximas gerações.")

    cols_per_row = 3
    rows = [modelos[i:i + cols_per_row] for i in range(0, len(modelos), cols_per_row)]

    for row in rows:
        cols = st.columns(cols_per_row, gap="medium")
        for col, modelo in zip(cols, row):
            is_ativa = modelo["id"] == ativa_id
            with col:
                # Badge de ativa
                if is_ativa:
                    st.markdown(
                        "<div style='background:#D4AF37;color:#fff;text-align:center;"
                        "border-radius:4px;padding:2px 8px;font-size:0.75rem;"
                        "font-weight:700;margin-bottom:4px;'>✅ ATIVA</div>",
                        unsafe_allow_html=True,
                    )

                # Preview
                st.image(
                    modelo["url"],
                    caption=modelo["nome"],
                    use_container_width=True,
                )
                st.caption(f"📅 {modelo.get('created_at', '—')}")

                # Botões
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if not is_ativa:
                        if st.button(
                            "✅ Usar",
                            key=f"usar_{modelo['id']}",
                            use_container_width=True,
                            type="primary",
                        ):
                            set_modelo_ativa(modelo["id"])
                            st.success(f"**{modelo['nome']}** selecionada!")
                            st.rerun()
                    else:
                        st.button(
                            "✅ Ativa",
                            key=f"ativa_{modelo['id']}",
                            use_container_width=True,
                            disabled=True,
                        )
                with btn_col2:
                    if st.button(
                        "🗑️",
                        key=f"del_{modelo['id']}",
                        use_container_width=True,
                        help=f"Excluir {modelo['nome']}",
                    ):
                        # Persiste remoção no Supabase se autenticado
                        if st.session_state.get("user_id"):
                            from src.services.supabase_client import delete_model_reference
                            delete_model_reference(modelo["id"])
                        remove_modelo_referencia(modelo["id"])
                        st.rerun()

    st.markdown("---")
else:
    st.info("👆 Você ainda não tem modelos cadastradas. Crie sua primeira modelo abaixo.")
    st.markdown("<br>", unsafe_allow_html=True)

# ─── Adicionar Nova Modelo ────────────────────────────────────────────────────

with st.expander("➕ Adicionar Nova Modelo", expanded=not modelos):
    tab_gerar, tab_upload = st.tabs(["✨ Gerar com IA", "📷 Usar minha foto"])

    # === Aba 1: Gerar com IA ===
    with tab_gerar:
        st.markdown("#### Descreva a modelo ideal para sua marca")

        col_form, col_prev = st.columns([1, 1], gap="large")

        with col_form:
            etnia = st.selectbox(
                "Aparência",
                ["Brasileira morena", "Brasileira loira", "Afro-brasileira",
                 "Latina", "Europeia", "Asiática"],
                key="new_modelo_etnia",
            )
            idade = st.selectbox(
                "Faixa etária",
                ["20-25 anos", "25-30 anos", "30-35 anos", "35-40 anos"],
                key="new_modelo_idade",
            )
            cabelo = st.selectbox(
                "Cabelo",
                ["Liso escuro", "Liso loiro", "Cacheado natural", "Crespo", "Ondulado castanho"],
                key="new_modelo_cabelo",
            )
            expressao = st.selectbox(
                "Expressão",
                ["Sorriso suave e elegante", "Olhar intenso e sofisticado",
                 "Expressão natural e serena", "Sorriso amplo e alegre"],
                key="new_modelo_expressao",
            )
            nome_modelo = st.text_input(
                "Nome para identificar",
                placeholder="Ex: Sofia — Modelo Principal",
                key="new_modelo_nome_ia",
            )

        with col_prev:
            st.info("💡 A modelo gerada será um retrato profissional em fundo branco neutro.")

        if st.button("✨ Gerar Modelo com IA", type="primary", key="btn_gerar_nova_modelo"):
            descricao = (
                f"{etnia} woman, {idade.replace(' anos', ' years old')}, "
                f"{cabelo.lower()} hair, {expressao.lower()}, "
                "professional headshot portrait, white background, "
                "photorealistic, 8k, commercial photography, sharp focus"
            )
            with st.spinner("🎨 Criando sua modelo exclusiva..."):
                from src.services.fal_client import fal_client
                result = fal_client.generate_model_from_text(descricao, num_images=1)

            if result.get("success") and result.get("images"):
                url = result["images"][0]["url"]
                nome = nome_modelo or f"{etnia}, {idade}"
                new_id = add_modelo_referencia(nome, url)

                # Persiste no Supabase se autenticado
                if st.session_state.get("user_id"):
                    from src.services.supabase_client import save_model_reference
                    save_model_reference(new_id, nome, url)

                logger.info(f"Nova modelo gerada e salva: {nome}")
                st.success(f"✅ **{nome}** criada e definida como ativa!")
                st.rerun()
            else:
                st.error(f"❌ Erro ao gerar modelo: {result.get('error')}")

    # === Aba 2: Upload ===
    with tab_upload:
        st.markdown("#### Use uma foto como referência de rosto")
        st.caption("Foto frontal com boa iluminação e rosto em destaque (PNG/JPG, máx 10MB)")

        uploaded_ref = st.file_uploader(
            "Selecione a foto de referência",
            type=["png", "jpg", "jpeg", "webp"],
            key="upload_nova_modelo_ref",
        )
        nome_upload = st.text_input(
            "Nome para identificar",
            placeholder="Ex: Valentina — Lookbook Verão",
            key="new_modelo_nome_upload",
        )

        if uploaded_ref is not None:
            validation = validate_image(uploaded_ref)
            if validation.is_valid:
                col_p, col_i = st.columns([1, 1], gap="large")
                with col_p:
                    st.image(uploaded_ref, caption="Prévia", use_container_width=True)
                with col_i:
                    st.success("✅ Foto válida.")
                    st.info(
                        "O rosto desta foto será usado pelo IP-Adapter FaceID do Fal.ai "
                        "para manter consistência em todas as gerações."
                    )

                if st.button("💾 Adicionar como Modelo", type="primary", key="btn_salvar_upload_nova"):
                    img_bytes = resize_image(uploaded_ref.getvalue())
                    img_b64 = to_base64(img_bytes)
                    nome = nome_upload or "Modelo de Referência"
                    new_id = add_modelo_referencia(nome, img_b64)

                    # Persiste no Supabase se autenticado
                    if st.session_state.get("user_id"):
                        from src.services.supabase_client import save_model_reference
                        save_model_reference(new_id, nome, img_b64)

                    logger.info(f"Nova modelo adicionada via upload: {nome}")
                    st.success(f"✅ **{nome}** adicionada e definida como ativa!")
                    st.rerun()
            else:
                st.error(f"❌ {validation.error_message}")

# ─── Navegação ────────────────────────────────────────────────────────────────

st.markdown("---")

modelo_ativa_atual = get_modelo_ativa()
if modelo_ativa_atual:
    col_info, col_btn = st.columns([3, 1])
    with col_info:
        st.success(f"**Modelo ativa:** {modelo_ativa_atual['nome']}")
    with col_btn:
        if st.button("Ir para Showroom →", type="primary", use_container_width=True, key="btn_ir_showroom"):
            st.switch_page("views/01_configuracao.py")
else:
    st.caption("⬆️ Adicione e selecione uma modelo para continuar.")
