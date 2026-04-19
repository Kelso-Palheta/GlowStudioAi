"""
============================================
GlowStudio AI - Login View
============================================
Página interceptadora para autenticação.
Apresenta UI elegante de acordo com a Luxury Boutique Edition.
"""

import streamlit as st
from src.services.supabase_client import sign_in, sign_up
import time

def render_login_page():
    # Centralized layout for login (Unified for zero-gap)
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 class="hero-title" style="margin-bottom: 0px !important; padding-bottom: 0px !important;">Acesso <span class="hero-highlight">Exclusivo</span></h1>
            <p class="hero-subtitle" style="margin-top: 0px !important; padding-top: 0.5rem !important;">Entre na sua conta para iniciar a curadoria boutique.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    col_spacer1, col_center, col_spacer2 = st.columns([1, 1.5, 1])

    with col_center:
        st.markdown('<div class="feature-card" style="padding: 1.5rem; margin-top: -1rem; background: white;">', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Entrar", "Criar Conta"])
        
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            email_login = st.text_input("E-mail", key="login_email")
            pass_login = st.text_input("Senha", type="password", key="login_pass")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Acessar GlowStudio", type="primary", use_container_width=True, key="btn_login"):
                if email_login and pass_login:
                    with st.spinner("Autenticando..."):
                        res = sign_in(email_login, pass_login)
                        if res.get("success"):
                            st.success("Acesso liberado!")
                            time.sleep(1)
                            st.rerun()  # Força o recarregamento (o app principal pegará a flag is_authenticated)
                        else:
                            st.error(res.get("error", "Erro ao entrar."))
                else:
                    st.warning("Preencha e-mail e senha.")
                    
        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            email_reg = st.text_input("E-mail", key="reg_email")
            pass_reg = st.text_input("Senha", type="password", key="reg_pass")
            pass_reg_conf = st.text_input("Confirme a Senha", type="password", key="reg_pass_conf")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Criar Conta", type="primary", use_container_width=True, key="btn_register"):
                if email_reg and pass_reg and pass_reg == pass_reg_conf:
                    with st.spinner("Criando credenciais..."):
                        res = sign_up(email_reg, pass_reg)
                        if res.get("success"):
                            st.success(res.get("message"))
                        else:
                            st.error(res.get("error", "Erro ao criar conta."))
                elif pass_reg != pass_reg_conf:
                    st.warning("As senhas não coincidem.")
                else:
                    st.warning("Preencha todos os campos.")
                    
        st.markdown('</div>', unsafe_allow_html=True)
        
if __name__ == "__main__":
    render_login_page()
