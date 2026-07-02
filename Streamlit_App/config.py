"""
config.py
---------
Central configuration for the House Price Prediction System.

Holds filesystem paths, app metadata, and design tokens. Nothing in this
file touches the ML backend — it only describes where the backend files
live so the rest of the app can find them.
"""

from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass

# -------------------------------------------------------------------------
# Filesystem paths
# -------------------------------------------------------------------------

BASE_DIR: Path = Path(__file__).resolve().parent          # Streamlit_App/
PROJECT_DIR: Path = BASE_DIR.parent                        # project root

MODEL_PATH: Path = PROJECT_DIR / "Model" / "house_price_model.pkl"
ENCODER_PATH: Path = PROJECT_DIR / "Model" / "label_encoders.pkl"
DATASET_PATH: Path = PROJECT_DIR / "Dataset" / "Housing.csv"

HISTORY_DIR: Path = BASE_DIR / "history"
HISTORY_FILE: Path = HISTORY_DIR / "predictions_history.json"

REPORTS_DIR: Path = BASE_DIR / "reports"
STYLES_DIR: Path = BASE_DIR / "styles"
ASSETS_DIR: Path = BASE_DIR / "assets"

HISTORY_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------------
# App metadata
# -------------------------------------------------------------------------

APP_NAME = "Estimate"
APP_TAGLINE = "AI-Powered House Price Intelligence"
APP_VERSION = "3.0.0"
APP_ICON = "🏠"
DEVELOPER_NAME = "Final Year AI & ML Project"
GITHUB_URL = "https://github.com/"

# The exact, immutable feature contract of the trained model.
# This mirrors model.feature_names_in_ and must never be reordered.
FEATURE_ORDER = [
    "area", "bedrooms", "bathrooms", "stories", "mainroad", "guestroom",
    "basement", "hotwaterheating", "airconditioning", "parking",
    "prefarea", "furnishingstatus",
]

BINARY_FIELDS = [
    "mainroad", "guestroom", "basement",
    "hotwaterheating", "airconditioning", "prefarea",
]

# -------------------------------------------------------------------------
# Design tokens (single source of truth for styles/theme.css + components)
# -------------------------------------------------------------------------


@dataclass(frozen=True)
class ThemeTokens:
    """Design tokens for a single theme (dark or light)."""
    bg: str
    bg_grid: str
    surface: str
    surface_border: str
    text_primary: str
    text_secondary: str
    accent: str          # blueprint cyan — primary interactive accent
    accent_soft: str
    gold: str             # valuation gold — reserved for price figures
    success: str
    danger: str


DARK_THEME = ThemeTokens(
    bg="#0B0F19",
    bg_grid="rgba(0, 217, 192, 0.05)",
    surface="rgba(255, 255, 255, 0.045)",
    surface_border="rgba(255, 255, 255, 0.09)",
    text_primary="#F3F5F7",
    text_secondary="#93A1B5",
    accent="#00D9C0",
    accent_soft="rgba(0, 217, 192, 0.14)",
    gold="#E8A33D",
    success="#3DDC97",
    danger="#FF6B6B",
)

LIGHT_THEME = ThemeTokens(
    bg="#F5F6F8",
    bg_grid="rgba(59, 130, 246, 0.05)",
    surface="rgba(255, 255, 255, 0.7)",
    surface_border="rgba(15, 23, 42, 0.08)",
    text_primary="#111827",
    text_secondary="#5B6472",
    accent="#0E9E8C",
    accent_soft="rgba(14, 158, 140, 0.12)",
    gold="#B9791E",
    success="#1E9E6A",
    danger="#D9483F",
)

FONT_DISPLAY = "'Space Grotesk', sans-serif"
FONT_BODY = "'Inter', sans-serif"
FONT_MONO = "'JetBrains Mono', monospace"

NAV_ITEMS = [
    {"label": "Dashboard", "icon": "🏛️", "page": "app.py"},
    {"label": "Predict", "icon": "🎯", "page": "pages/1_Predict.py"},
    {"label": "Analytics", "icon": "📊", "page": "pages/2_Analytics.py"},
    {"label": "Reports", "icon": "📄", "page": "pages/3_Reports.py"},
    {"label": "History", "icon": "🕘", "page": "pages/4_History.py"},
    {"label": "Model Info", "icon": "🧠", "page": "pages/7_Model_Info.py"},
    {"label": "Architecture", "icon": "🛠️", "page": "pages/8_Architecture.py"},
    {"label": "Settings", "icon": "⚙️", "page": "pages/5_Settings.py"},
    {"label": "About", "icon": "ℹ️", "page": "pages/6_About.py"},
]

ACCENT_CHOICES = [
    {"name": "Cyan", "color": "#00D9C0", "soft": "rgba(0, 217, 192, 0.14)"},
    {"name": "Purple", "color": "#8B5CF6", "soft": "rgba(139, 92, 246, 0.12)"},
    {"name": "Sunset", "color": "#F59E0B", "soft": "rgba(245, 158, 11, 0.14)"},
    {"name": "Rose", "color": "#EC4899", "soft": "rgba(236, 72, 153, 0.14)"},
]

DEFAULT_ACCENT = "Cyan"
