"""
components/cards.py
--------------------
Reusable presentational building blocks: glass cards, stat chips,
badges, and the prediction result panel. Pure UI — no ML logic.
"""

from __future__ import annotations

import streamlit as st

from utils.formatting import format_inr, format_inr_short, humanize_timestamp


def render_hero(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="est-hero">
            <div class="est-eyebrow">{eyebrow}</div>
            <div class="est-display" style="font-size:38px; font-weight:700; line-height:1.15;">
                {title}
            </div>
            <div class="est-body" style="font-size:16px; max-width:640px; margin-top:10px;">
                {subtitle}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stat_card(label: str, value: str, icon: str = "📈") -> None:
    st.markdown(
        f"""
        <div class="est-card" style="text-align:left;">
            <div style="font-size:20px;">{icon}</div>
            <div class="est-stat-value" style="margin-top:6px;">{value}</div>
            <div class="est-stat-label" style="margin-top:2px;">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_price_panel(predicted_price: float, timestamp: str | None = None) -> None:
    ts_html = (
        f'<div class="est-mono" style="font-size:12px; margin-top:10px; color:var(--text-secondary);">'
        f'Predicted on {humanize_timestamp(timestamp)}</div>'
        if timestamp else ""
    )
    st.markdown(
        f"""
        <div class="est-price-panel">
            <div class="est-eyebrow">Estimated Market Value</div>
            <div class="est-price-value">{format_inr(predicted_price)}</div>
            <div class="est-body" style="font-size:13px;">≈ {format_inr_short(predicted_price)}</div>
            {ts_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_info_card(title: str, body_html: str, icon: str = "🏠") -> None:
    st.markdown(
        f"""
        <div class="est-card">
            <div style="font-size:20px; margin-bottom:6px;">{icon}</div>
            <div class="est-display" style="font-size:16px; font-weight:700; margin-bottom:6px;">
                {title}
            </div>
            <div class="est-body" style="font-size:14px; line-height:1.55;">{body_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
