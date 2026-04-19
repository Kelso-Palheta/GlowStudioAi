"""
============================================
GlowStudio AI - Header Component
============================================
Skill 1: UI/UX Streamlit (Frontend)

Barra de progresso visual + branding inline.
Reutilizável em todas as telas do workflow.
"""

import streamlit as st


def render_progress_header(current_step: int, total_steps: int = 3):
    """
    Renderiza um header com barra de progresso visual das etapas.
    Ref: Estética Semijoias Light Premium.
    """
    steps = [
        {"num": 1, "label": "SHOWROOM", "icon": "💎"},
        {"num": 2, "label": "CURADORIA", "icon": "✨"},
        {"num": 3, "label": "ESTÚDIO", "icon": "👑"},
    ]

    items = []
    for step in steps[:total_steps]:
        state = "pending"
        icon = step["icon"]
        
        if step["num"] < current_step:
            state = "completed"
            icon = "💎"
        elif step["num"] == current_step:
            state = "active"

        step_html = f'<div class="progress-step {state}"><div class="step-circle">{icon}</div><div class="step-label">{step["label"]}</div></div>'
        items.append(step_html)
        
        if step["num"] < total_steps:
            conn_state = "completed" if step["num"] < current_step else ""
            items.append(f'<div class="step-connector {conn_state}"></div>')

    # Container centralizado e sem restrições que quebrem o flex
    full_html = f'<div class="progress-bar-container">{"".join(items)}</div>'
    
    st.markdown(full_html, unsafe_allow_html=True)
