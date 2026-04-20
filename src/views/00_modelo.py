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

        # ── Características Essenciais ──
        st.markdown("**Características Essenciais**")
        col1, col2, col3 = st.columns(3)
        with col1:
            etnia = st.selectbox("Aparência / Etnia", [
                "Brasileira morena", "Brasileira loira", "Afro-brasileira",
                "Latina", "Europeia", "Asiática", "Árabe", "Mediterrânea",
            ], key="new_modelo_etnia")
            tom_pele = st.selectbox("Tom de pele", [
                "Clara", "Morena clara", "Morena", "Morena escura", "Negra",
            ], key="new_modelo_tom_pele")
        with col2:
            idade = st.selectbox("Faixa etária", [
                "18-22 anos", "22-27 anos", "27-32 anos", "32-38 anos", "38-45 anos",
            ], key="new_modelo_idade")
            altura = st.selectbox("Altura / Porte", [
                "Baixa e delicada (1,55–1,60)", "Média (1,60–1,68)",
                "Alta (1,68–1,75)", "Alta e esguia (1,75+)",
            ], key="new_modelo_altura")
        with col3:
            corpo = st.selectbox("Tipo de corpo", [
                "Esguia / Magra", "Atlética / Definida", "Mediana / Natural",
                "Curvilínea", "Plus Size", "Ampulheta",
            ], key="new_modelo_corpo")
            expressao = st.selectbox("Expressão", [
                "Sorriso suave e elegante", "Olhar intenso e sofisticado",
                "Expressão natural e serena", "Sorriso amplo e alegre",
                "Olhar sensual", "Pose editorial séria",
            ], key="new_modelo_expressao")

        st.markdown("---")

        # ── Rosto ──
        st.markdown("**Detalhes do Rosto**")
        col4, col5, col6 = st.columns(3)
        with col4:
            formato_rosto = st.selectbox("Formato do rosto", [
                "Oval", "Redondo", "Coração", "Quadrado", "Longo / Fino",
            ], key="new_modelo_rosto")
            labios = st.selectbox("Lábios", [
                "Naturais e finos", "Médios", "Carnudos / Volumosos",
                "Boca larga e sensual",
            ], key="new_modelo_labios")
        with col5:
            olhos_cor = st.selectbox("Cor dos olhos", [
                "Castanhos escuros", "Castanhos claros", "Pretos",
                "Verdes", "Azuis", "Mel / Âmbar", "Cinza",
            ], key="new_modelo_olhos_cor")
            olhos_formato = st.selectbox("Formato dos olhos", [
                "Amendoado", "Grandes e expressivos", "Pequenos e delicados",
                "Felinos / Puxados",
            ], key="new_modelo_olhos_formato")
        with col6:
            sobrancelhas = st.selectbox("Sobrancelhas", [
                "Finas e arqueadas", "Médias naturais", "Grossas e marcadas",
                "Retas e modernas",
            ], key="new_modelo_sobrancelhas")
            maquiagem = st.selectbox("Maquiagem", [
                "Sem maquiagem / Natural", "Leve e luminosa",
                "Elegante / Clássica", "Dramática / Marcada",
                "Smoky eye sofisticado",
            ], key="new_modelo_maquiagem")

        st.markdown("---")

        # ── Cabelo ──
        st.markdown("**Cabelo**")
        col7, col8, col9 = st.columns(3)
        with col7:
            cabelo_cor = st.selectbox("Cor do cabelo", [
                "Preto", "Castanho escuro", "Castanho claro", "Loiro dourado",
                "Loiro platinado", "Ruivo", "Mechas / Balayage", "Colorido",
            ], key="new_modelo_cabelo_cor")
        with col8:
            cabelo_tipo = st.selectbox("Tipo / Textura", [
                "Liso e sedoso", "Liso e volumoso", "Ondulado",
                "Cacheado", "Crespo / Afro", "Enrolado tight",
            ], key="new_modelo_cabelo_tipo")
        with col9:
            cabelo_comprimento = st.selectbox("Comprimento", [
                "Curto (pixie/bob)", "Médio (até o ombro)",
                "Longo (até o peito)", "Muito longo (abaixo da cintura)",
            ], key="new_modelo_cabelo_comprimento")

        st.markdown("---")

        nome_modelo = st.text_input(
            "Nome para identificar esta modelo",
            placeholder="Ex: Sofia — Modelo Principal",
            key="new_modelo_nome_ia",
        )

        if st.button("✨ Gerar Modelo com IA", type="primary", key="btn_gerar_nova_modelo"):
            idade_en = idade.split(" ")[0].replace("-", " to ") + " years old"
            altura_en = altura.split("(")[0].strip().lower()
            descricao = (
                f"{etnia} woman, {idade_en}, {tom_pele.lower()} skin tone, "
                f"{altura_en}, {corpo.lower()} body type, "
                f"{formato_rosto.lower()} face shape, {olhos_cor.lower()} {olhos_formato.lower()} eyes, "
                f"{sobrancelhas.lower()} eyebrows, {labios.lower()} lips, "
                f"{cabelo_comprimento.lower()} {cabelo_tipo.lower()} {cabelo_cor.lower()} hair, "
                f"{maquiagem.lower()}, {expressao.lower()}, "
                "professional headshot portrait, white studio background, "
                "photorealistic, 8k, commercial jewelry photography, sharp focus"
            )
            with st.spinner("🎨 Criando sua modelo exclusiva..."):
                from src.services.fal_client import fal_client
                result = fal_client.generate_model_from_text(descricao, num_images=1)

            if result.get("success") and result.get("images"):
                url = result["images"][0]["url"]
                nome = nome_modelo or f"{etnia}, {cabelo_cor.lower()}, {idade}"
                new_id = add_modelo_referencia(nome, url)
                if st.session_state.get("user_id"):
                    from src.services.supabase_client import save_model_reference
                    save_model_reference(new_id, nome, url)
                logger.info(f"Nova modelo gerada: {nome}")
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
