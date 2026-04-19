"""
============================================
GlowStudio AI - Supabase Client
============================================
Gerenciamento de conexão com o banco de dados Supabase
e funções de Autenticação.
"""

from supabase import create_client, Client
import streamlit as st
import os
from src.config.settings import settings
from src.utils.logger import get_logger
from src.services.session_manager import init_session_state

logger = get_logger(__name__)

# Cache the connection to avoid recreating the client on every rerun
def get_supabase_client() -> Client:
    """Inicializa e retorna o cliente Supabase."""
    from dotenv import load_dotenv
    from pathlib import Path
    
    # Força recarregamento do .env na hora da conexão para depurar
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    load_dotenv(env_path, override=True)
    
    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_KEY", "").strip()
    
    if not url or not key:
        logger.warning("Credenciais do Supabase ausentes ou vazias no .env.")
        return None
        
    try:
        supabase: Client = create_client(url, key)
        # Seta a sessão se existir no state para garantir regras de RLS
        if "supabase_session" in st.session_state and st.session_state["supabase_session"]:
            session = st.session_state["supabase_session"]
            if hasattr(session, 'access_token') and hasattr(session, 'refresh_token'):
                try:
                    supabase.auth.set_session(session.access_token, session.refresh_token)
                except Exception:
                    pass
        return supabase
    except Exception as e:
        logger.error(f"Erro ao conectar ao Supabase: {e}")
        return None

def sign_up(email: str, password: str) -> dict:
    """Cria um novo usuário."""
    supabase = get_supabase_client()
    if not supabase:
        return {"success": False, "error": "Banco de dados não configurado."}
        
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        if res.user:
            return {"success": True, "message": "Conta criada! Verifique seu e-mail para confirmar."}
        return {"success": False, "error": "Falha na criação da conta."}
    except Exception as e:
        logger.error(f"Erro no Sign Up: {e}")
        return {"success": False, "error": str(e)}

def sign_in(email: str, password: str) -> dict:
    """Realiza o login do usuário."""
    supabase = get_supabase_client()
    if not supabase:
        # Mock behavior for local testing if keys are missing
        st.session_state["is_authenticated"] = True
        st.session_state["user_email"] = email
        return {"success": True}
        
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if res.session:
            st.session_state["is_authenticated"] = True
            st.session_state["user_id"] = res.user.id
            st.session_state["user_email"] = res.user.email
            st.session_state["supabase_session"] = res.session
            logger.info(f"Usuário {email} logado com sucesso.")
            return {"success": True}
        return {"success": False, "error": "Credenciais inválidas ou e-mail não confirmado."}
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Erro no Sign In: {error_msg}")
        # Simplifica mensagens comuns para o usuário
        if "Email not confirmed" in error_msg:
            return {"success": False, "error": "E-mail ainda não confirmado. Verifique sua caixa de entrada!"}
        return {"success": False, "error": "E-mail ou senha incorretos."}

def sign_out():
    """Realiza o logout do usuário com limpeza total de estado."""
    supabase = get_supabase_client()
    if supabase:
        try:
            supabase.auth.sign_out()
        except Exception as e:
            logger.error(f"Erro no Sign Out remote: {e}")
            
    # Limpeza agressiva do session_state (Skill 2)
    keys_to_clear = [
        "is_authenticated", "user_id", "user_email", 
        "supabase_session", "imagens_geradas", "video_gerado",
        "legenda_gerada", "prompt_visual"
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
            
    # Reseta flags de controle
    st.session_state["texto_aprovado"] = False
    st.session_state["processando"] = False
    
    logger.info("Sessão encerrada e dados limpos (Logout).")

def check_session():
    """Verifica se há uma sessão ativa remota e atualiza o estado."""
    # Preserva o estado se o usuário já validou o login nesta sessão do app
    if st.session_state.get("is_authenticated") and st.session_state.get("user_id"):
        return
        
    supabase = get_supabase_client()
    if not supabase:
        return
        
    try:
        res = supabase.auth.get_session()
        if res and res.session:
            st.session_state["is_authenticated"] = True
            st.session_state["user_id"] = res.session.user.id
            st.session_state["user_email"] = res.session.user.email
            st.session_state["supabase_session"] = res.session
    except Exception:
        pass

def save_generation(
    gen_type: str,
    image_url: str = None,
    caption: str = None,
    prompt: str = None,
    marketing_objective: str = None,
    target_audience: str = None,
    features: list = None,
    original_image_url: str = None
) -> dict:
    """Salva uma nova geração no banco de dados."""
    supabase = get_supabase_client()
    if not supabase or not st.session_state.get("user_id"):
        return {"success": False, "error": "Usuário não autenticado ou banco offline."}
        
    try:
        data = {
            "user_id": st.session_state["user_id"],
            "type": gen_type,
            "image_url": image_url,
            "caption": caption,
            "prompt": prompt,
            "marketing_objective": marketing_objective,
            "target_audience": target_audience,
            "features": features or [],
            "original_image_url": original_image_url
        }
        res = supabase.table("generations").insert(data).execute()
        if res.data:
            logger.info(f"Geração {gen_type} salva com sucesso para o usuário {st.session_state['user_id']}.")
            return {"success": True, "data": res.data}
        return {"success": False, "error": "Falha ao salvar no banco."}
    except Exception as e:
        logger.error(f"Erro ao salvar geração: {e}")
        return {"success": False, "error": str(e)}

def get_user_history(limit: int = 20) -> list:
    """Recupera o histórico de gerações do usuário logado."""
    supabase = get_supabase_client()
    if not supabase or not st.session_state.get("user_id"):
        return []
        
    try:
        res = supabase.table("generations")\
            .select("*")\
            .eq("user_id", st.session_state["user_id"])\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        return res.data if res.data else []
    except Exception as e:
        logger.error(f"Erro ao recuperar histórico: {e}")
        return []
