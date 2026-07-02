"""
pages/7_Model_Info.py
---------------------
Dedicated model information page with algorithm, feature lists,
training metadata, and workflow overview.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from config import (
    APP_ICON,
    APP_NAME,
    DATASET_PATH,
    FEATURE_ORDER,
)
from components.assistant import render_ai_assistant
from components.navigation import resolve_query_nav
from components.navbar import render_navbar
from components.styling import inject_global_styles
from components.header import render_header
from components.sidebar import render_sidebar
from components.cards import render_hero, render_info_card
from components.footer import render_footer
from services.model_service import load_model_and_encoders

st.set_page_config(page_title=f"Model Info · {APP_NAME}", page_icon=APP_ICON, layout="wide")

inject_global_styles()
resolve_query_nav("pages/7_Model_Info.py")
render_sidebar()
render_navbar()
render_header()
render_ai_assistant()

model, label_encoders = load_model_and_encoders()

render_hero(
    eyebrow="Model Information",
    title="Know what powers the predictions",
    subtitle="A transparent view into the model, the dataset, and the features used for estimation.",
)

try:
    df = pd.read_csv(DATASET_PATH)
except FileNotFoundError:
    st.error(f"Dataset not found at `{DATASET_PATH}`.")
    st.stop()

categorical = [col for col in FEATURE_ORDER if df[col].dtype == 'object']
numeric = [col for col in FEATURE_ORDER if df[col].dtype != 'object']

col1, col2 = st.columns(2)
with col1:
    render_info_card(
        "Algorithm",
        f"<b>{type(model).__name__}</b><br>Persisted from the training pipeline, loaded at runtime.",
        icon="🧠",
    )
    render_info_card(
        "Dataset",
        f"{len(df):,} records · {len(df.columns)} columns · Indian housing data.",
        icon="🗂️",
    )

with col2:
    render_info_card(
        "Features Used",
        ", ".join(FEATURE_ORDER),
        icon="📌",
    )
    render_info_card(
        "Categorical Features",
        ", ".join(categorical) if categorical else "None",
        icon="🧷",
    )

st.write("")

st.markdown("##### 📈 Summary Statistics")
st.dataframe(df.describe(include='all').transpose(), use_container_width=True)

st.write("")

st.markdown("##### 🔧 Model Metadata")
model_info = {
    "Feature order": FEATURE_ORDER,
    "Label encoders": list(label_encoders.keys()),
    "Supports coefficients": hasattr(model, "coef_"),
    "Supports feature importances": hasattr(model, "feature_importances_"),
}

for key, value in model_info.items():
    st.markdown(f"- **{key}**: {value}")

st.write("")

if hasattr(model, "coef_"):
    st.markdown("##### 📊 Linear Coefficients")
    coeffs = dict(zip(model.feature_names_in_, model.coef_))
    st.table(pd.DataFrame.from_dict(coeffs, orient='index', columns=['Coefficient']))
else:
    st.info("The loaded model does not expose linear coefficients.")

render_footer()
