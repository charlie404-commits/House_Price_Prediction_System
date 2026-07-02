"""
pages/3_Reports.py
-------------------
Download center: export a single prediction as PDF, or the full
history as CSV.
"""

from __future__ import annotations

import streamlit as st

from config import APP_NAME, APP_ICON
from components.assistant import render_ai_assistant
from components.navigation import resolve_query_nav
from components.navbar import render_navbar
from components.styling import inject_global_styles
from components.header import render_header
from components.sidebar import render_sidebar
from components.cards import render_hero, render_info_card
from components.footer import render_footer
from utils.storage import get_history, history_to_csv_bytes
from utils.formatting import format_inr, humanize_timestamp
from utils.report_generator import build_prediction_pdf

st.set_page_config(page_title=f"Reports · {APP_NAME}", page_icon=APP_ICON, layout="wide")

inject_global_styles()
resolve_query_nav("pages/3_Reports.py")
render_sidebar()
render_navbar()
render_header()
render_ai_assistant()

render_hero(
    eyebrow="Reports",
    title="Download center",
    subtitle="Export a single prediction as a polished PDF, or your full history as CSV.",
)

records = get_history()

if not records:
    render_info_card(
        "No predictions yet",
        "Run a prediction on the <b>Predict</b> page first — it will show up here for export.",
        icon="📄",
    )
    render_footer()
    st.stop()

col_left, col_right = st.columns([1.3, 1])

with col_left:
    st.markdown("##### 📄 Single Prediction Report")
    options = {
        f"{humanize_timestamp(r['timestamp'])} — {format_inr(r['predicted_price'])}": r
        for r in records
    }
    choice_label = st.selectbox("Choose a prediction", list(options.keys()))
    chosen = options[choice_label]

    pdf_bytes = build_prediction_pdf(chosen)
    st.download_button(
        "⬇️ Download PDF Report",
        data=pdf_bytes,
        file_name=f"house_price_report_{chosen['id'][:8]}.pdf",
        mime="application/pdf",
        use_container_width=True,
        type="primary",
    )

with col_right:
    st.markdown("##### 🗂️ Full History (CSV)")
    csv_bytes = history_to_csv_bytes()
    st.download_button(
        "⬇️ Download History CSV",
        data=csv_bytes,
        file_name="prediction_history.csv",
        mime="text/csv",
        use_container_width=True,
    )
    st.caption(f"{len(records)} prediction(s) in history.")

render_footer()
