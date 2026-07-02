"""
services/model_service.py
--------------------------
Loads the FINAL, production ML backend artifacts.

This module intentionally contains no business logic beyond loading —
it does not retrain, does not modify, and does not reinterpret the
model or encoders in any way. It is a thin, cached I/O boundary.
"""

from __future__ import annotations

from typing import Any, Dict, Tuple

import joblib
import streamlit as st

from config import MODEL_PATH, ENCODER_PATH


@st.cache_resource(show_spinner=False)
def load_model_and_encoders() -> Tuple[Any, Dict[str, Any]]:
    """
    Load the trained regression model and label encoders exactly as they
    were produced by the training notebook.

    Cached via st.cache_resource so the model is loaded once per process,
    not once per user interaction.

    Returns:
        (model, label_encoders)
    """
    try:
        model = joblib.load(MODEL_PATH)
        encoders = joblib.load(ENCODER_PATH)
        return model, encoders
    except FileNotFoundError:
        st.error("❌ Model files not found.")
        st.info(
            f"Expected files:\n\n- `{MODEL_PATH}`\n- `{ENCODER_PATH}`\n\n"
            "Run the training notebook first to generate them."
        )
        st.stop()
    except Exception as exc:  # noqa: BLE001 — surfaced to the user, then halted
        st.error(f"❌ Error loading model: {exc}")
        st.stop()


def get_furnishing_options(label_encoders: Dict[str, Any]) -> list[str]:
    """Return the exact furnishing status categories the model was trained on."""
    return list(label_encoders["furnishingstatus"].classes_)
