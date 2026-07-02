"""
components/header.py
---------------------
Renders the top-of-page header: brand mark, version badge, and current date.
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from config import APP_NAME, APP_TAGLINE, APP_VERSION, APP_ICON, GITHUB_URL


def render_header() -> None:
    today = datetime.now().strftime("%d %b %Y")

    st.markdown(
        f"""
        <div class="est-card est-card--flat" style="display:flex; align-items:center;
             justify-content:space-between; padding:16px 24px; margin-bottom:22px;">
            <div style="display:flex; align-items:center; gap:12px;">
                <span style="font-size:26px;">{APP_ICON}</span>
                <img src="/Streamlit_App/assets/anime_character.svg" alt="anime" style="width:44px; height:44px; margin-left:6px;"/>
                <div>
                    <div class="est-display" style="font-size:19px; font-weight:700; line-height:1.1;">
                        {APP_NAME}
                    </div>
                    <div class="est-mono" style="font-size:11.5px; color:var(--text-secondary);">
                        {APP_TAGLINE}
                    </div>
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:10px;">
                <span class="est-badge">{today}</span>
                <span class="est-badge est-badge--accent">v{APP_VERSION}</span>
                <a href="{GITHUB_URL}" target="_blank" style="text-decoration:none;">
                    <span class="est-badge">GitHub ↗</span>
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
