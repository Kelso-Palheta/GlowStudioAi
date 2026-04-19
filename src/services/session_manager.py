"""
GlowStudio AI - Session Manager
Gerenciamento centralizado do st.session_state.
"""

import uuid
import streamlit as st
from datetime import date
from typing import Optional, Dict, Any, List
from src.utils.logger import get_logger

logger = get_logger(__name__)

_DEFAULT_STATE = {
    # --- Autenticação ---
    "is_authenticated": False,
    "user_id": None,
    "user_email": None,

    # --- Etapa 0: Minhas Modelos ---
    "modelos_referencia": [],        # lista de dicts: {id, nome, url, created_at}
    "modelo_ativa_id": None,         # ID da modelo selecionada atualmente
    "modelo_referencia_url": None,   # URL da modelo ativa (usado pelo pipeline)
    "modelos_carregados": False,     # flag: já carregou do Supabase?

    # --- Tela 1: Configuração Estratégica ---
    "uploaded_image": None,
    "uploaded_filename": "",
    "objetivo": "",
    "publico": "",
    "diferenciais": [],

    # --- Tela 2: Direção de Arte e Look ---
    "cenario": "",
    "look": "",
    "legenda_gerada": "",
    "prompt_visual": "",
    "texto_aprovado": False,

    # --- Tela 3: Estúdio de Resultados ---
    "imagens_geradas": [],
    "video_gerado": None,

    # --- Controle de Navegação ---
    "etapa_atual": 1,
    "processando": False,
    "erros": [],
}

# Chaves que NÃO devem ser limpas ao resetar o workflow
_PRESERVE_ON_RESET = {
    "is_authenticated", "user_id", "user_email",
    "modelos_referencia", "modelo_ativa_id",
    "modelo_referencia_url", "modelos_carregados",
}


def init_session_state():
    """Inicializa o session_state com valores padrão (não sobrescreve existentes)."""
    for key, default_value in _DEFAULT_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
    logger.debug("Session state inicializado")


def reset_session():
    """Limpa dados do workflow mas preserva autenticação e modelos de referência."""
    for key, default_value in _DEFAULT_STATE.items():
        if key not in _PRESERVE_ON_RESET:
            st.session_state[key] = default_value
    logger.info("Session state resetado (modelos e auth preservados)")


# ─── Funções de Modelos de Referência ────────────────────────────────────────

def get_modelos() -> List[Dict[str, Any]]:
    """Retorna a lista de todas as modelos de referência da sessão."""
    return st.session_state.get("modelos_referencia", [])


def get_modelo_ativa() -> Optional[Dict[str, Any]]:
    """Retorna o dict da modelo atualmente ativa, ou None."""
    ativa_id = st.session_state.get("modelo_ativa_id")
    if not ativa_id:
        return None
    for m in get_modelos():
        if m["id"] == ativa_id:
            return m
    return None


def set_modelo_ativa(model_id: str) -> bool:
    """Define a modelo ativa por ID e atualiza modelo_referencia_url. Retorna True se encontrou."""
    for m in get_modelos():
        if m["id"] == model_id:
            st.session_state["modelo_ativa_id"] = model_id
            st.session_state["modelo_referencia_url"] = m["url"]
            logger.info(f"Modelo ativa: {m['nome']} ({model_id})")
            return True
    return False


def add_modelo_referencia(nome: str, url: str, model_id: str = None) -> str:
    """Adiciona uma nova modelo à lista, define como ativa e retorna seu ID."""
    new_id = model_id or str(uuid.uuid4())
    novo = {
        "id": new_id,
        "nome": nome,
        "url": url,
        "created_at": str(date.today()),
    }
    if "modelos_referencia" not in st.session_state:
        st.session_state["modelos_referencia"] = []
    st.session_state["modelos_referencia"].append(novo)
    set_modelo_ativa(new_id)
    logger.info(f"Modelo adicionada: {nome} ({new_id})")
    return new_id


def remove_modelo_referencia(model_id: str):
    """Remove uma modelo da lista. Se era a ativa, seleciona a próxima disponível."""
    st.session_state["modelos_referencia"] = [
        m for m in get_modelos() if m["id"] != model_id
    ]
    if st.session_state.get("modelo_ativa_id") == model_id:
        st.session_state["modelo_ativa_id"] = None
        st.session_state["modelo_referencia_url"] = None
        remaining = get_modelos()
        if remaining:
            set_modelo_ativa(remaining[0]["id"])
    logger.info(f"Modelo removida: {model_id}")


def load_modelos_from_supabase():
    """Carrega modelos do Supabase para a sessão (executa apenas uma vez por sessão)."""
    if st.session_state.get("modelos_carregados"):
        return
    if not st.session_state.get("user_id"):
        return
    try:
        from src.services.supabase_client import get_user_models
        models = get_user_models()
        for m in models:
            # Só adiciona se ainda não estiver na lista local
            ids_existentes = {x["id"] for x in get_modelos()}
            if m["id"] not in ids_existentes:
                st.session_state["modelos_referencia"].append(m)
        # Restaura a ativa se havia uma
        if get_modelos() and not st.session_state.get("modelo_ativa_id"):
            set_modelo_ativa(get_modelos()[0]["id"])
        st.session_state["modelos_carregados"] = True
        logger.info(f"{len(models)} modelos carregadas do Supabase")
    except Exception as e:
        logger.warning(f"Não foi possível carregar modelos do Supabase: {e}")


# ─── Funções genéricas ────────────────────────────────────────────────────────

def set_etapa(etapa: int):
    if etapa not in (1, 2, 3):
        raise ValueError(f"Etapa inválida: {etapa}. Use 1, 2 ou 3.")
    st.session_state["etapa_atual"] = etapa
    logger.debug(f"Navegação: etapa → {etapa}")


def get_etapa() -> int:
    return st.session_state.get("etapa_atual", 1)


def add_error(message: str):
    if "erros" not in st.session_state:
        st.session_state["erros"] = []
    st.session_state["erros"].append(message)
    logger.error(f"Erro adicionado à sessão: {message}")


def clear_errors():
    st.session_state["erros"] = []


def has_uploaded_image() -> bool:
    return st.session_state.get("uploaded_image") is not None


def has_modelo_referencia() -> bool:
    """Verifica se há pelo menos uma modelo e uma está ativa."""
    return bool(st.session_state.get("modelo_referencia_url"))
