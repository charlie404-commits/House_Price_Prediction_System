"""
components/navigation.py
------------------------
Helper to resolve query-param-driven page navigation in the Streamlit
multipage app so custom nav links can remain functional.
"""

from __future__ import annotations

import streamlit as st

from config import NAV_ITEMS


def _get_query_params() -> dict[str, list[str]]:
    if hasattr(st, "experimental_get_query_params"):
        return st.experimental_get_query_params()
    return st.query_params


def _set_query_params(params: dict[str, str | int | bool | list[str] | tuple[str, ...]]) -> None:
    if hasattr(st, "experimental_set_query_params"):
        st.experimental_set_query_params(**params)
        return

    normalized_params: dict[str, list[str]] = {}
    for key, value in params.items():
        if isinstance(value, (list, tuple)):
            normalized_params[key] = [str(item) for item in value]
        else:
            normalized_params[key] = [str(value)]

    st.query_params = normalized_params


def resolve_query_nav(current_page: str) -> None:
    params = _get_query_params()
    target = params.get("page", [None])[0]
    if not target or target == current_page:
        return

    allowed_pages = {item["page"] for item in NAV_ITEMS}
    if target not in allowed_pages:
        return

    _set_query_params({"page": target})
    st.switch_page(target)
