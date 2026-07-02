"""
components/styling.py
----------------------
Injects design-token CSS variables + the shared stylesheet into the page.
Also owns the tiny bit of session state that tracks dark/light theme.
"""

from __future__ import annotations

from dataclasses import replace

import streamlit as st

from config import (
    ACCENT_CHOICES,
    DARK_THEME,
    DEFAULT_ACCENT,
    LIGHT_THEME,
    FONT_BODY,
    FONT_DISPLAY,
    FONT_MONO,
    STYLES_DIR,
)


def get_theme_name() -> str:
    return st.session_state.get("theme", "dark")


def set_theme_name(name: str) -> None:
    st.session_state["theme"] = name


def get_accent_name() -> str:
    return st.session_state.get("accent", DEFAULT_ACCENT)


def set_accent_name(name: str) -> None:
    st.session_state["accent"] = name


def get_animations_enabled() -> bool:
    return st.session_state.get("animations_enabled", True)


def set_animations_enabled(enabled: bool) -> None:
    st.session_state["animations_enabled"] = enabled


def _active_tokens():
    theme_tokens = DARK_THEME if get_theme_name() == "dark" else LIGHT_THEME
    accent_choice = next(
        (item for item in ACCENT_CHOICES if item["name"] == get_accent_name()),
        ACCENT_CHOICES[0],
    )
    return replace(
        theme_tokens,
        accent=accent_choice["color"],
        accent_soft=accent_choice["soft"],
    )


def inject_global_styles() -> None:
    """Inject CSS variables for the active theme, then the shared stylesheet."""
    tokens = _active_tokens()

    css_vars = f"""
    <style>
    :root {{
        --bg: {tokens.bg};
        --bg-grid: {tokens.bg_grid};
        --surface: {tokens.surface};
        --surface-border: {tokens.surface_border};
        --text-primary: {tokens.text_primary};
        --text-secondary: {tokens.text_secondary};
        --accent: {tokens.accent};
        --accent-soft: {tokens.accent_soft};
        --gold: {tokens.gold};
        --success: {tokens.success};
        --danger: {tokens.danger};
        --font-display: {FONT_DISPLAY};
        --font-body: {FONT_BODY};
        --font-mono: {FONT_MONO};
    }}
    </style>
    """
    st.markdown(css_vars, unsafe_allow_html=True)

    if not get_animations_enabled():
        st.markdown(
            "<style>* { animation: none !important; transition: none !important; }</style>",
            unsafe_allow_html=True,
        )

    theme_css_path = STYLES_DIR / "theme.css"
    if theme_css_path.exists():
        css = theme_css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
