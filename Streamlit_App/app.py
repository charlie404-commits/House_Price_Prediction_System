"""
app.py
------
Dashboard / Home page — entry point for the House Price Prediction System.

This file only orchestrates UI. The ML backend is loaded via
services/model_service.py and never modified here.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from config import APP_NAME, APP_ICON, DATASET_PATH
from components.assistant import render_ai_assistant
from components.navigation import resolve_query_nav
from components.navbar import render_navbar
from components.styling import inject_global_styles
from components.header import render_header
from components.sidebar import render_sidebar
from components.cards import render_hero, render_stat_card, render_info_card
from components.footer import render_footer
from services.model_service import load_model_and_encoders
from utils.storage import get_history_df

# -------------------------------------------------------------------------
# Page configuration (must be the first Streamlit call)
# -------------------------------------------------------------------------

st.set_page_config(
    page_title=f"{APP_NAME} · House Price Prediction",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_styles()
resolve_query_nav("app.py")
render_sidebar()
render_navbar()
render_header()

# -------------------------------------------------------------------------
# Load backend (cached — loaded once per process)
# -------------------------------------------------------------------------

model, label_encoders = load_model_and_encoders()

# -------------------------------------------------------------------------
# Hero
# -------------------------------------------------------------------------

render_hero(
    eyebrow="AI · Machine Learning · Real Estate",
    title="Know a house's worth before you ever see the listing.",
    subtitle=(
        "A production-style dashboard around a trained regression model — "
        "enter a property's details and get an instant, data-driven price estimate."
    ),
)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🎯 Start a Prediction", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Predict.py")
with col2:
    if st.button("📊 View Analytics", use_container_width=True):
        st.switch_page("pages/2_Analytics.py")

st.write("")

# -------------------------------------------------------------------------
# Quick statistics
# -------------------------------------------------------------------------

try:
    dataset = pd.read_csv(DATASET_PATH)
except FileNotFoundError:
    dataset = pd.DataFrame()

history_df = get_history_df()

stat_cols = st.columns(4)
with stat_cols[0]:
    render_stat_card("Training Records", f"{len(dataset):,}" if not dataset.empty else "—", "🗂️")
with stat_cols[1]:
    avg_price = f"₹{dataset['price'].mean():,.0f}" if "price" in dataset else "—"
    render_stat_card("Average Price", avg_price, "💰")
with stat_cols[2]:
    model_name = type(model).__name__
    render_stat_card("Model", model_name, "🧠")
with stat_cols[3]:
    render_stat_card("Predictions Made", f"{len(history_df)}" if not history_df.empty else "0", "🕘")

st.write("")

# -------------------------------------------------------------------------
# Feature overview
# -------------------------------------------------------------------------

st.markdown("#### What this dashboard offers")
info_cols = st.columns(3)
with info_cols[0]:
    render_info_card(
        "Instant Predictions",
        "Enter area, bedrooms, amenities and more to get a price estimate "
        "in Indian Rupees, powered by the trained model.",
        icon="🎯",
    )
with info_cols[1]:
    render_info_card(
        "Data Analytics",
        "Explore distributions, correlations, and how price relates to "
        "each feature in the underlying dataset.",
        icon="📊",
    )
with info_cols[2]:
    render_info_card(
        "History & Reports",
        "Every prediction is saved to your history, with CSV/PDF export "
        "for sharing or record-keeping.",
        icon="📄",
    )

render_footer()
render_ai_assistant()
