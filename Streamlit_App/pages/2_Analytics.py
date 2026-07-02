"""
pages/2_Analytics.py
---------------------
Read-only, interactive view of the training dataset and the model's
learned coefficients. This page never retrains or mutates the model —
it only visualizes what already exists.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from config import APP_NAME, APP_ICON, DATASET_PATH, FEATURE_ORDER
from components.assistant import render_ai_assistant
from components.navigation import resolve_query_nav
from components.navbar import render_navbar
from components.styling import inject_global_styles
from components.header import render_header
from components.sidebar import render_sidebar
from components.cards import render_hero, render_stat_card
from components.footer import render_footer
from services.model_service import load_model_and_encoders

st.set_page_config(page_title=f"Analytics · {APP_NAME}", page_icon=APP_ICON, layout="wide")

inject_global_styles()
resolve_query_nav("pages/2_Analytics.py")
render_sidebar()
render_navbar()
render_header()
render_ai_assistant()

model, label_encoders = load_model_and_encoders()

render_hero(
    eyebrow="Analytics",
    title="Understand the training data",
    subtitle="Interactive charts over the dataset the model was trained on — no retraining happens here.",
)

try:
    df = pd.read_csv(DATASET_PATH)
except FileNotFoundError:
    st.error(f"Dataset not found at `{DATASET_PATH}`.")
    st.stop()

# -------------------------------------------------------------------------
# Summary stats
# -------------------------------------------------------------------------

stat_cols = st.columns(4)
with stat_cols[0]:
    render_stat_card("Rows", f"{len(df):,}", "🗂️")
with stat_cols[1]:
    render_stat_card("Avg Price", f"₹{df['price'].mean():,.0f}", "💰")
with stat_cols[2]:
    render_stat_card("Avg Area", f"{df['area'].mean():,.0f} sqft", "📐")
with stat_cols[3]:
    render_stat_card("Max Price", f"₹{df['price'].max():,.0f}", "🏆")

st.write("")
st.markdown('<div class="est-card">', unsafe_allow_html=True)
st.markdown("##### 🔍 Dataset Preview")
st.dataframe(df.head(20), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# -------------------------------------------------------------------------
# Distributions
# -------------------------------------------------------------------------

st.markdown("##### 📊 Feature Distributions")
dist_col1, dist_col2 = st.columns(2)

with dist_col1:
    fig_area = px.histogram(df, x="area", nbins=30, title="Area Distribution",
                             color_discrete_sequence=["#00D9C0"])
    fig_area.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)", height=340)
    st.plotly_chart(fig_area, use_container_width=True)

    fig_bath = px.histogram(df, x="bathrooms", title="Bathrooms Distribution",
                             color_discrete_sequence=["#E8A33D"])
    fig_bath.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)", height=340)
    st.plotly_chart(fig_bath, use_container_width=True)

with dist_col2:
    fig_bed = px.histogram(df, x="bedrooms", title="Bedrooms Distribution",
                            color_discrete_sequence=["#00D9C0"])
    fig_bed.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                           plot_bgcolor="rgba(0,0,0,0)", height=340)
    st.plotly_chart(fig_bed, use_container_width=True)

    fig_park = px.histogram(df, x="parking", title="Parking Distribution",
                             color_discrete_sequence=["#E8A33D"])
    fig_park.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)", height=340)
    st.plotly_chart(fig_park, use_container_width=True)

# -------------------------------------------------------------------------
# Correlation heatmap
# -------------------------------------------------------------------------

st.markdown("##### 🔥 Correlation Heatmap (numeric features)")
numeric_df = df.select_dtypes(include="number")
corr = numeric_df.corr()
fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale="Teal", aspect="auto")
fig_corr.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)", height=460)
st.plotly_chart(fig_corr, use_container_width=True)

# -------------------------------------------------------------------------
# Model coefficients (only if the model exposes them)
# -------------------------------------------------------------------------

st.markdown("##### 🧠 Model Coefficients")
if hasattr(model, "coef_"):
    coef_df = pd.DataFrame({
        "feature": getattr(model, "feature_names_in_", FEATURE_ORDER),
        "coefficient": model.coef_,
    }).sort_values("coefficient", key=abs, ascending=True)

    fig_coef = px.bar(
        coef_df, x="coefficient", y="feature", orientation="h",
        title="Linear Regression Coefficients (impact on predicted price)",
        color="coefficient", color_continuous_scale="Teal",
    )
    fig_coef.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)", height=440)
    st.plotly_chart(fig_coef, use_container_width=True)
    st.caption(
        "This model is a Linear Regression, so bars show learned coefficients "
        "(how much predicted price shifts per unit increase in that feature), "
        "not tree-based feature importance."
    )
else:
    st.info("The loaded model does not expose linear coefficients or feature importances.")

render_footer()
