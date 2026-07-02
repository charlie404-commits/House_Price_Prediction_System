"""
pages/6_About.py
-----------------
Project narrative: dataset, workflow, algorithms, tech stack, and
architecture — informational only.
"""

from __future__ import annotations

import streamlit as st

from config import APP_NAME, APP_ICON, DEVELOPER_NAME
from components.assistant import render_ai_assistant
from components.navigation import resolve_query_nav
from components.navbar import render_navbar
from components.styling import inject_global_styles
from components.header import render_header
from components.sidebar import render_sidebar
from components.cards import render_hero, render_info_card
from components.footer import render_footer

st.set_page_config(page_title=f"About · {APP_NAME}", page_icon=APP_ICON, layout="wide")

inject_global_styles()
resolve_query_nav("pages/6_About.py")
render_sidebar()
render_navbar()
render_header()
render_ai_assistant()

render_hero(
    eyebrow="About",
    title="How this project works",
    subtitle="From raw housing data to a deployed prediction dashboard.",
)

c1, c2 = st.columns(2)
with c1:
    render_info_card(
        "Dataset",
        "545 records of Indian housing sales with 12 features — area, "
        "bedrooms, bathrooms, stories, amenities (main road, guest room, "
        "basement, hot water heating, air conditioning, preferred area), "
        "parking, and furnishing status.",
        icon="🗂️",
    )
with c2:
    render_info_card(
        "Workflow",
        "Data Loading → Cleaning → EDA → Outlier Removal (IQR) → "
        "Feature Encoding → Train/Test Split (80/20) → Model Training → "
        "Evaluation (MAE, MSE, RMSE, R²) → Best Model Selection → "
        "Persistence (joblib) → Streamlit Deployment.",
        icon="🔄",
    )

st.write("")
c3, c4 = st.columns(2)
with c3:
    render_info_card(
        "Algorithms Compared",
        "Linear Regression, Random Forest Regressor, and XGBoost Regressor "
        "were trained and evaluated; the best performer was persisted as "
        "the production model.",
        icon="🧠",
    )
with c4:
    render_info_card(
        "Technologies",
        "Python · pandas · numpy · scikit-learn · XGBoost · joblib · "
        "Streamlit · Plotly · fpdf2.",
        icon="🛠️",
    )

st.write("")
st.markdown("##### 🏗️ Architecture")
st.markdown(
    """
    <div class="est-card est-mono" style="font-size:13px; line-height:1.7; white-space:pre;">
Notebook (training, offline)
  Dataset/Housing.csv → House_Price_Prediction.ipynb → Model/*.pkl

Streamlit_App (serving, this dashboard)
  services/model_service.py       loads Model/*.pkl (cached)
  services/prediction_service.py  encode → reorder → predict
  pages/*.py                      UI screens
  components/, utils/, styles/    reusable UI + formatting + storage
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
c5, c6 = st.columns(2)
with c5:
    render_info_card("Developer", DEVELOPER_NAME, icon="👤")
with c6:
    render_info_card(
        "Future Scope",
        "Swap in a database for cross-device history, add authentication, "
        "support live retraining pipelines, and expand to multi-city datasets.",
        icon="🚀",
    )

render_footer()
