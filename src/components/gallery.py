"""
============================================
GlowStudio AI - Gallery Component
============================================
Skill 1: UI/UX Streamlit (Frontend)

Galeria de imagens genérica com grid responsivo,
botões de download e ação por imagem.
"""

import streamlit as st
from typing import List, Dict, Any, Optional, Callable


def render_gallery(
    images: List[Dict[str, Any]],
    columns: int = 2,
    show_download: bool = True,
    show_action: bool = False,
    action_label: str = "🎬 Animar",
    action_callback: Optional[Callable] = None,
    action_disabled: bool = False,
):
    """
    Renderiza uma galeria de imagens em grid.

    Args:
        images: Lista de dicts com 'url' ou 'bytes' e opcionalmente 'seed'
        columns: Número de colunas do grid
        show_download: Mostrar botão de download
        show_action: Mostrar botão de ação (ex: Animar)
        action_label: Label do botão de ação
        action_callback: Função chamada ao clicar na ação
        action_disabled: Se True, desabilita o botão de ação
    """
    if not images:
        st.info("📷 Nenhuma imagem para exibir.")
        return

    cols = st.columns(columns, gap="medium")

    for idx, img_data in enumerate(images):
        with cols[idx % columns]:
            # Renderiza a imagem
            img_source = img_data.get("url", img_data.get("bytes", ""))
            st.image(
                img_source,
                caption=f"Variação {idx + 1}",
                use_container_width=True,
            )

            # Botões abaixo da imagem
            btn_cols = []
            if show_download and show_action:
                btn_cols = st.columns(2)
            elif show_download or show_action:
                btn_cols = [st.columns(1)[0]]

            btn_idx = 0
            if show_download:
                container = btn_cols[btn_idx] if btn_cols else st
                with container:
                    img_bytes = img_data.get("bytes", b"")
                    if img_bytes:
                        st.download_button(
                            "📥 Download",
                            data=img_bytes,
                            file_name=f"glowstudio_{idx + 1}.png",
                            mime="image/png",
                            key=f"gallery_dl_{idx}",
                            use_container_width=True,
                        )
                btn_idx += 1

            if show_action:
                container = btn_cols[btn_idx] if len(btn_cols) > btn_idx else st
                with container:
                    if st.button(
                        action_label,
                        key=f"gallery_action_{idx}",
                        use_container_width=True,
                        disabled=action_disabled,
                    ):
                        if action_callback:
                            action_callback(idx, img_data)
