"""
utils/storage.py
-----------------
Lightweight persistence for prediction history.

Stored as a JSON file under Streamlit_App/history/ so predictions survive
across app restarts without requiring a database or backend change.
"""

from __future__ import annotations

import io
import json
import uuid
from typing import Any, Dict, List

import pandas as pd

from config import HISTORY_FILE
from utils.formatting import now_timestamp


def _read_all() -> List[Dict[str, Any]]:
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _write_all(records: List[Dict[str, Any]]) -> None:
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)


def add_record(inputs: Dict[str, Any], predicted_price: float) -> Dict[str, Any]:
    """Append a new prediction record and return it."""
    record = {
        "id": str(uuid.uuid4()),
        "timestamp": now_timestamp(),
        "predicted_price": predicted_price,
        **inputs,
    }
    records = _read_all()
    records.insert(0, record)  # newest first
    _write_all(records)
    return record


def get_history() -> List[Dict[str, Any]]:
    return _read_all()


def get_history_df() -> pd.DataFrame:
    records = _read_all()
    if not records:
        return pd.DataFrame()
    return pd.DataFrame(records)


def delete_record(record_id: str) -> None:
    records = [r for r in _read_all() if r.get("id") != record_id]
    _write_all(records)


def clear_history() -> None:
    _write_all([])


def history_to_csv_bytes() -> bytes:
    df = get_history_df()
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")
