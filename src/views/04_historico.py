"""
============================================
GlowStudio AI - Histórico de Joias
============================================
Exibição das gerações passadas do usuário logado.
Design: Luxury Boutique Edition (Skill 1).
"""

import streamlit as st
from src.services.supabase_client import get_user_history
import datetime

def render_historico_page():
    st.markdown(
        """
        <div class="page-header" style="text-align: center; padding: 2rem 1rem;">
            <h1 class="page-title">Histórico de <span class="hero-highlight">Excelência</span></h1>
            <p class="hero-subtitle">Veja suas criações exclusivas.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    history = get_user_history(limit=40)

    if not history:
        st.info("Você ainda não possui gerações no seu histórico. Comece sua primeira curadoria!")
        if st.button("✨ Iniciar Agora", type="primary"):
            st.switch_page("src/views/01_configuracao.py")
        return

    # Filtros e Estatísticas Rápidas
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Total de Peças", len(history))
    
    st.markdown("---")

    # Grid de Histórico (Skill 1: Luxury Edition)
    # Mostramos em colunas para simular uma galeria de luxo
    cols = st.columns(3)
    
    for idx, item in enumerate(history):
        col_idx = idx % 3
        with cols[col_idx]:
            with st.container(border=True):
                # Imagem
                if item.get("image_url"):
                    st.image(item["image_url"], use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/400x400?text=Sem+Imagem", use_container_width=True)
                
                # Detalhes
                data_criacao = datetime.datetime.fromisoformat(item["created_at"].replace("Z", "+00:00"))
                st.markdown(f"**📅 {data_criacao.strftime('%d/%m/%Y')}**")
                
                if item.get("marketing_objective"):
                    st.caption(f"🎯 {item['marketing_objective']} | {item.get('target_audience', 'Público Geral')}")
                
                # Expandir para ver legenda
                with st.expander("📄 Ver Legenda"):
                    st.write(item.get("caption", "Sem legenda salva."))
                    if st.button("Copiar Legenda", key=f"copy_{item['id']}"):
                        st.toast("Legenda copiada para a área de transferência!")
                        # Nota: st.copy_to_clipboard está chegando em versões novas, 
                        # por enquanto simular com toast.
                
                # Botão Deletar (UX)
                if st.button("🗑️", key=f"del_{item['id']}", help="Remover do histórico"):
                    # Aqui chamaríamos uma função de delete no futuro
                    st.warning("Função de exclusão em breve.")

    st.markdown("---")
    st.markdown('<p style="text-align: center; color: var(--text-secondary); font-size: 0.8rem;">GlowStudio AI • Private Collection</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    render_historico_page()
