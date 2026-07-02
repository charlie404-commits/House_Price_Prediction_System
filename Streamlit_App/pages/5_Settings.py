"""
pages/5_Settings.py
--------------------
App preferences: theme, history reset, and version/build info.
"""

from __future__ import annotations

import streamlit as st

from config import APP_NAME, APP_ICON, APP_VERSION, MODEL_PATH, ENCODER_PATH, DATASET_PATH
from components.assistant import render_ai_assistant
from components.navigation import resolve_query_nav
from components.navbar import render_navbar
from components.styling import inject_global_styles, get_theme_name, set_theme_name
from components.header import render_header
from components.sidebar import render_sidebar
from components.cards import render_hero, render_info_card
from components.footer import render_footer
from utils.storage import clear_history, get_history

st.set_page_config(page_title=f"Settings · {APP_NAME}", page_icon=APP_ICON, layout="wide")

inject_global_styles()
resolve_query_nav("pages/5_Settings.py")
render_sidebar()
render_navbar()
render_header()
render_ai_assistant()

render_hero(
    eyebrow="Settings",
    title="Preferences",
    subtitle="Personalize the dashboard and manage local data.",
)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="est-card">', unsafe_allow_html=True)
    st.markdown("##### 🎨 Appearance")
    is_dark = get_theme_name() == "dark"
    choice = st.radio("Theme", ["Dark", "Light"], index=0 if is_dark else 1, horizontal=True)
    set_theme_name("dark" if choice == "Dark" else "light")
    st.caption("Accent color is derived from the design tokens in config.py.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="est-card">', unsafe_allow_html=True)
    st.markdown("##### 🗑️ Data Management")
    n_records = len(get_history())
    st.caption(f"{n_records} prediction(s) currently stored locally.")
    if st.button("Reset Prediction History", type="secondary"):
        clear_history()
        st.success("History cleared.")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    render_info_card(
        "Version Information",
        f"""
        <table style="width:100%; font-size:13.5px;">
            <tr><td style="padding:4px 0;">App Version</td><td style="text-align:right;">{APP_VERSION}</td></tr>
            <tr><td style="padding:4px 0;">Model File</td><td style="text-align:right;">{MODEL_PATH.name}</td></tr>
            <tr><td style="padding:4px 0;">Encoders File</td><td style="text-align:right;">{ENCODER_PATH.name}</td></tr>
            <tr><td style="padding:4px 0;">Dataset File</td><td style="text-align:right;">{DATASET_PATH.name}</td></tr>
        </table>
        """,
        icon="ℹ️",
    )

render_footer()
