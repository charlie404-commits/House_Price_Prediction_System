"""
components/footer.py
---------------------
Renders the shared page footer.
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from config import APP_NAME, APP_VERSION, DEVELOPER_NAME, GITHUB_URL


def render_footer() -> None:
    year = datetime.now().year
    st.markdown('<hr class="est-divider">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="est-footer">
            {APP_NAME} v{APP_VERSION} · {DEVELOPER_NAME} ·
            <a href="{GITHUB_URL}" target="_blank" style="color:var(--accent); text-decoration:none;">GitHub</a>
            · © {year}
        </div>
        """,
        unsafe_allow_html=True,
    )
