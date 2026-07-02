"""
components/navbar.py
--------------------
Top navigation bar for the startup-style AI real estate platform.
"""

from __future__ import annotations

import streamlit as st

from config import NAV_ITEMS


def render_navbar() -> None:
    nav_html = """
    <div class="est-nav-shell">
        <div class="est-nav-brand">
            <div class="est-nav-logo">🏡</div>
            <div>
                <div class="est-nav-title">Estimate</div>
                <div class="est-nav-subtitle">AI Real Estate Platform</div>
            </div>
        </div>
        <div class="est-nav-links">
    """

    for item in NAV_ITEMS:
        nav_html += (
            f"<a class='est-nav-link' href='?page={item['page']}'>{item['icon']} {item['label']}</a>"
        )

    nav_html += """
        </div>
    </div>
    """
    st.markdown(nav_html, unsafe_allow_html=True)
