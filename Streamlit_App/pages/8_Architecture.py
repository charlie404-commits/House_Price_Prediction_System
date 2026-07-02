"""
pages/8_Architecture.py
-----------------------
Architecture page describing dataset, preprocessing, training,
and deployment flow for the AI real estate platform.
"""

from __future__ import annotations

import streamlit as st

from config import APP_ICON, APP_NAME
from components.assistant import render_ai_assistant
from components.navigation import resolve_query_nav
from components.navbar import render_navbar
from components.styling import inject_global_styles
from components.header import render_header
from components.sidebar import render_sidebar
from components.cards import render_hero, render_info_card
from components.footer import render_footer

st.set_page_config(page_title=f"Architecture · {APP_NAME}", page_icon=APP_ICON, layout="wide")

inject_global_styles()
resolve_query_nav("pages/8_Architecture.py")
render_sidebar()
render_navbar()
render_header()
render_ai_assistant()

render_hero(
    eyebrow="Project Architecture",
    title="How data flows through the platform",
    subtitle="A production-inspired architecture overview with dataset, model, and deployment boundaries.",
)

st.markdown("##### 🚀 System Flow")
st.markdown(
    """
    <div class='est-card'>
        <div class='est-display' style='font-size:18px;'>Data & Deployment Pipeline</div>
        <div class='est-body' style='margin-top:12px; white-space:pre-line;'>
Dataset (Housing.csv) → Training Notebook → Model Persistence (joblib)
→ Streamlit Service Layer
→ Prediction Service → User Interface
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

st.markdown("##### 🧩 Architecture Components")
col1, col2, col3 = st.columns(3)
with col1:
    render_info_card(
        "Dataset",
        "Housing.csv is loaded from the Dataset folder and analyzed in the notebook. No dataset changes occur in production.",
        icon="📁",
    )
with col2:
    render_info_card(
        "Preprocessing",
        "Raw inputs are encoded using persisted LabelEncoders and reordered to match the model contract.",
        icon="⚙️",
    )
with col3:
    render_info_card(
        "Prediction",
        "The runtime service only performs inference with the loaded model — no retraining or feature engineering occurs here.",
        icon="📡",
    )

st.write("")

st.markdown("##### 🧠 Deployment")
render_info_card(
    "Serving",
    "Streamlit hosts the UI and loads the persisted model with st.cache_resource for efficient inference.",
    icon="🌐",
)

render_footer()
