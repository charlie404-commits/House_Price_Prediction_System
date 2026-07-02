"""
pages/4_History.py
-------------------
Browse, search, sort, delete, and export past predictions.
Backed by utils/storage.py (JSON file under Streamlit_App/history/).
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
from utils.storage import get_history, delete_record, clear_history, history_to_csv_bytes
from utils.formatting import format_inr, humanize_timestamp

st.set_page_config(page_title=f"History · {APP_NAME}", page_icon=APP_ICON, layout="wide")

inject_global_styles()
resolve_query_nav("pages/4_History.py")
render_sidebar()
render_navbar()
render_header()
render_ai_assistant()

render_hero(
    eyebrow="History",
    title="Your prediction history",
    subtitle="Every estimate you've generated, searchable and exportable.",
)

records = get_history()

if not records:
    render_info_card(
        "Nothing here yet",
        "Predictions you make on the <b>Predict</b> page will appear here automatically.",
        icon="🕘",
    )
    render_footer()
    st.stop()

# -------------------------------------------------------------------------
# Controls
# -------------------------------------------------------------------------

ctrl1, ctrl2, ctrl3 = st.columns([2, 1, 1])
with ctrl1:
    search = st.text_input("🔍 Search (furnishing, main road, etc.)", "")
with ctrl2:
    sort_by = st.selectbox("Sort by", ["Newest first", "Oldest first", "Price: High to Low", "Price: Low to High"])
with ctrl3:
    st.write("")
    st.write("")
    if st.button("🗑️ Clear All History", use_container_width=True):
        clear_history()
        st.rerun()

filtered = records
if search:
    needle = search.lower()
    filtered = [r for r in records if needle in str(r).lower()]

if sort_by == "Oldest first":
    filtered = list(reversed(filtered))
elif sort_by == "Price: High to Low":
    filtered = sorted(filtered, key=lambda r: r["predicted_price"], reverse=True)
elif sort_by == "Price: Low to High":
    filtered = sorted(filtered, key=lambda r: r["predicted_price"])

st.caption(f"Showing {len(filtered)} of {len(records)} prediction(s)")

st.download_button(
    "⬇️ Export filtered view as CSV",
    data=history_to_csv_bytes(),
    file_name="prediction_history.csv",
    mime="text/csv",
)

st.write("")

# -------------------------------------------------------------------------
# Records list
# -------------------------------------------------------------------------

for record in filtered:
    with st.container():
        st.markdown('<div class="est-card" style="margin-bottom:14px;">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 3, 1])
        with c1:
            st.markdown(
                f"<div class='est-stat-value' style='font-size:22px;'>{format_inr(record['predicted_price'])}</div>"
                f"<div class='est-mono' style='font-size:11.5px; color:var(--text-secondary);'>"
                f"{humanize_timestamp(record['timestamp'])}</div>",
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f"<span class='est-badge'>{record['area']} sqft</span> "
                f"<span class='est-badge'>{record['bedrooms']} bed</span> "
                f"<span class='est-badge'>{record['bathrooms']} bath</span> "
                f"<span class='est-badge'>{record['stories']} stories</span> "
                f"<span class='est-badge'>{record['furnishingstatus']}</span>",
                unsafe_allow_html=True,
            )
        with c3:
            if st.button("Delete", key=f"del_{record['id']}", use_container_width=True):
                delete_record(record["id"])
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

render_footer()
