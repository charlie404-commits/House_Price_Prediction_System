"""
components/sidebar.py
----------------------
Sidebar branding block + theme toggle. Page links themselves are
rendered automatically by Streamlit's native multipage navigation
(the pages/ folder); this just adds a polished brand header above it
and a light/dark toggle.
"""

from __future__ import annotations

import streamlit as st

from config import ACCENT_CHOICES, APP_ICON, APP_NAME, APP_VERSION, NAV_ITEMS
from components.styling import (
    get_accent_name,
    get_animations_enabled,
    get_theme_name,
    set_accent_name,
    set_animations_enabled,
    set_theme_name,
)


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding:18px 12px 14px 12px;">
                <div style="font-size:30px;">{APP_ICON}</div>
                <div class="est-display" style="font-size:22px; font-weight:700; margin-top:10px;">
                    {APP_NAME}
                </div>
                <div class="est-mono" style="font-size:12px; color:var(--text-secondary); margin-top:6px;">
                    v{APP_VERSION} · AI Real Estate
                </div>
            </div>
            <hr class="est-divider" style="margin-top:16px; margin-bottom:18px;">
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### Quick links")
        for item in NAV_ITEMS:
            st.markdown(
                f"<div class='sidebar-link'>• <a href='?page={item['page']}'>{item['icon']} {item['label']}</a></div>",
                unsafe_allow_html=True,
            )

        st.markdown('<hr class="est-divider">', unsafe_allow_html=True)

        st.markdown("##### Theme")
        is_dark = get_theme_name() == "dark"
        theme_choice = st.radio(
            "Mode",
            ["Dark", "Light"],
            index=0 if is_dark else 1,
            horizontal=True,
        )
        set_theme_name("dark" if theme_choice == "Dark" else "light")

        accent_names = [choice["name"] for choice in ACCENT_CHOICES]
        accent_choice = st.selectbox("Accent", accent_names, index=accent_names.index(get_accent_name()))
        set_accent_name(accent_choice)

        anim_enabled = get_animations_enabled()
        animations = st.checkbox("Enable animations", value=anim_enabled)
        set_animations_enabled(animations)

        st.markdown('<hr class="est-divider">', unsafe_allow_html=True)
        st.caption("Pro navigation, project theming, and local state persist across pages.")
