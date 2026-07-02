"""
services/prediction_service.py
-------------------------------
Wraps the ORIGINAL, unmodified prediction pipeline from the working
app.py in a reusable, testable function:

    1. Build a single-row DataFrame from raw user inputs.
    2. Encode categorical columns with the trained LabelEncoders.
    3. Reorder columns to model.feature_names_in_.
    4. model.predict(...)

No preprocessing step, encoding order, or feature order has been
changed from the original implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import pandas as pd


@dataclass(frozen=True)
class HouseFeatures:
    """Raw, human-entered inputs for a single prediction request."""
    area: int
    bedrooms: int
    bathrooms: int
    stories: int
    mainroad: str
    guestroom: str
    basement: str
    hotwaterheating: str
    airconditioning: str
    parking: int
    prefarea: str
    furnishingstatus: str

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame({
            "area": [self.area],
            "bedrooms": [self.bedrooms],
            "bathrooms": [self.bathrooms],
            "stories": [self.stories],
            "mainroad": [self.mainroad],
            "guestroom": [self.guestroom],
            "basement": [self.basement],
            "hotwaterheating": [self.hotwaterheating],
            "airconditioning": [self.airconditioning],
            "parking": [self.parking],
            "prefarea": [self.prefarea],
            "furnishingstatus": [self.furnishingstatus],
        })


def predict_price(model: Any, label_encoders: Dict[str, Any], features: HouseFeatures) -> float:
    """
    Run the exact original prediction pipeline and return the predicted price.

    This mirrors app.py's original logic 1:1:
        input_df -> label-encode each known column -> reorder to
        model.feature_names_in_ -> model.predict()
    """
    input_df = features.to_frame()

    # Encode categorical columns (identical to the original implementation)
    for column in label_encoders:
        input_df[column] = label_encoders[column].transform(input_df[column])

    # Reorder columns to match training (identical to the original implementation)
    if hasattr(model, "feature_names_in_"):
        input_df = input_df[model.feature_names_in_]

    prediction = model.predict(input_df)[0]
    return float(prediction)
