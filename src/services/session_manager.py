"""
============================================
GlowStudio AI - Session Manager
============================================
Gerenciamento centralizado do st.session_state.
Estrutura definida no Documento Mestre, Seção 6.4.
"""

import streamlit as st
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Estrutura padrão do session_state
_DEFAULT_STATE = {
    # --- Autenticação ---
    "is_authenticated": False,
    "user_id": None,
    "user_email": None,
    
    # --- Tela 1: Configuração Estratégica ---
    "uploaded_image": None,          # bytes da imagem original
    "uploaded_filename": "",         # nome do arquivo
    "objetivo": "",                  # objetivo de marketing selecionado
    "publico": "",                   # público-alvo selecionado
    "diferenciais": [],              # lista de diferenciais marcados

    # --- Tela 2: Edição e Aprovação ---
    "legenda_gerada": "",            # texto de vendas da Maritaca AI
    "prompt_visual": "",             # prompt de imagem da Maritaca AI
    "texto_aprovado": False,         # flag: usuário aprovou o texto?

    # --- Tela 3: Estúdio de Resultados ---
    "imagens_geradas": [],           # lista de URLs/bytes das imagens
    "video_gerado": None,            # bytes do vídeo animado

    # --- Controle de Navegação ---
    "etapa_atual": 1,                # controle de navegação (1, 2 ou 3)
    "processando": False,            # flag de loading
    "erros": [],                     # lista de erros para exibição
}


def init_session_state():
    """Inicializa o session_state com valores padrão.
    
    Deve ser chamado uma vez no início do app (app.py).
    Só inicializa chaves que ainda não existem, preservando dados
    entre reruns do Streamlit.
    """
    for key, default_value in _DEFAULT_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
    
    logger.debug("Session state inicializado")


def reset_session():
    """Limpa todos os dados da sessão para iniciar um novo workflow.
    
    Usado quando o usuário quer começar do zero (novo upload, nova geração).
    """
    for key, default_value in _DEFAULT_STATE.items():
        st.session_state[key] = default_value
    
    logger.info("Session state resetado pelo usuário")


def set_etapa(etapa: int):
    """Define a etapa atual do workflow.
    
    Args:
        etapa: Número da etapa (1, 2 ou 3)
        
    Raises:
        ValueError: Se a etapa não for 1, 2 ou 3
    """
    if etapa not in (1, 2, 3):
        raise ValueError(f"Etapa inválida: {etapa}. Use 1, 2 ou 3.")
    
    st.session_state["etapa_atual"] = etapa
    logger.debug(f"Navegação: etapa → {etapa}")


def get_etapa() -> int:
    """Retorna a etapa atual do workflow.
    
    Returns:
        Número da etapa atual (1, 2 ou 3)
    """
    return st.session_state.get("etapa_atual", 1)


def add_error(message: str):
    """Adiciona uma mensagem de erro à lista de erros da sessão.
    
    Args:
        message: Mensagem de erro para exibir ao usuário
    """
    if "erros" not in st.session_state:
        st.session_state["erros"] = []
    st.session_state["erros"].append(message)
    logger.error(f"Erro adicionado à sessão: {message}")


def clear_errors():
    """Limpa todas as mensagens de erro da sessão."""
    st.session_state["erros"] = []


def has_uploaded_image() -> bool:
    """Verifica se há uma imagem carregada na sessão.
    
    Returns:
        True se existe imagem no session_state
    """
    return st.session_state.get("uploaded_image") is not None
