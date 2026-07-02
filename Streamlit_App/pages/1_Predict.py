"""
pages/1_Predict.py
-------------------
The core prediction workflow. UI only — the prediction math is delegated
to services/prediction_service.py, which is a 1:1 wrap of the original
app.py logic (encode -> reorder -> predict).
"""

from __future__ import annotations

import time

import streamlit as st

from config import APP_NAME, APP_ICON
from components.assistant import render_ai_assistant
from components.navigation import resolve_query_nav
from components.navbar import render_navbar
from components.styling import inject_global_styles
from components.header import render_header
from components.sidebar import render_sidebar
from components.cards import render_hero, render_price_panel
from components.footer import render_footer
from components.voice_input import render_voice_input
from services.model_service import load_model_and_encoders, get_furnishing_options
from services.prediction_service import HouseFeatures, predict_price
from utils.storage import add_record
from utils.voice_parser import parse_voice_command

st.set_page_config(page_title=f"Predict · {APP_NAME}", page_icon=APP_ICON, layout="wide")

inject_global_styles()
resolve_query_nav("pages/1_Predict.py")
render_sidebar()
render_navbar()
render_header()
render_ai_assistant()

model, label_encoders = load_model_and_encoders()

render_hero(
    eyebrow="Predict",
    title="Estimate a property's price",
    subtitle="Use text or voice to enter property details, then get a polished AI price estimate.",
)

render_voice_input()

voice_command = st.text_area(
    "Voice or natural language description",
    placeholder="Speak or type property description",
    help="Example: Area 2500 square feet, three bedrooms, two bathrooms, parking two, semi furnished.",
    key="voice_command",
)

parsed_inputs = parse_voice_command(voice_command) if voice_command else {}
full_voice_fields = [
    "area", "bedrooms", "bathrooms", "stories", "parking",
    "mainroad", "guestroom", "basement", "hotwaterheating",
    "airconditioning", "prefarea", "furnishingstatus",
]
voice_has_all_fields = bool(parsed_inputs and all(field in parsed_inputs for field in full_voice_fields))

if st.session_state.get("voice_command") != st.session_state.get("last_voice_command"):
    st.session_state["voice_auto_submit_executed"] = False
    st.session_state["voice_confirmed"] = False
    st.session_state["last_voice_command"] = st.session_state.get("voice_command")

if voice_has_all_fields:
    st.session_state["voice_auto_submit_ready"] = True
else:
    st.session_state["voice_auto_submit_ready"] = False

voice_confirm = st.session_state.get("voice_confirmed", False)
if parsed_inputs:
    st.success("Parsed input: " + ", ".join(f"{k}={v}" for k, v in parsed_inputs.items()))
    if voice_has_all_fields:
        st.info('Full property details were detected from your voice input and will be submitted automatically.')
    else:
        st.warning('Partial property details were detected. Review or press the button below to use recognized values and submit.')

    if st.button("Use recognized values and submit", type="primary", key="voice_confirm_button"):
        st.session_state["voice_confirmed"] = True
        voice_confirm = True

# -------------------------------------------------------------------------
# Input form
# -------------------------------------------------------------------------

with st.form("prediction_form"):
    st.markdown("##### 📐 Property Basics")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        area = st.number_input(
            "Area (sq ft)",
            min_value=500,
            max_value=20000,
            value=parsed_inputs.get("area", 5000),
            step=50,
            help="Total built-up area of the property in square feet.",
        )
    with c2:
        bedrooms = st.number_input(
            "Bedrooms",
            min_value=1,
            max_value=10,
            value=parsed_inputs.get("bedrooms", 3),
            help="Number of bedrooms.",
        )
    with c3:
        bathrooms = st.number_input(
            "Bathrooms",
            min_value=1,
            max_value=10,
            value=parsed_inputs.get("bathrooms", 2),
            help="Number of bathrooms.",
        )
    with c4:
        stories = st.number_input(
            "Stories",
            min_value=1,
            max_value=5,
            value=parsed_inputs.get("stories", 2),
            help="Number of floors/stories.",
        )

    st.markdown("##### 🧰 Amenities")
    a1, a2, a3 = st.columns(3)
    with a1:
        mainroad = st.selectbox(
            "Main Road",
            ["yes", "no"],
            index=0 if parsed_inputs.get("mainroad") == "yes" else 1,
            help="Does the property face a main road?",
        )
        guestroom = st.selectbox(
            "Guest Room",
            ["yes", "no"],
            index=0 if parsed_inputs.get("guestroom") == "yes" else 1,
        )
    with a2:
        basement = st.selectbox(
            "Basement",
            ["yes", "no"],
            index=0 if parsed_inputs.get("basement") == "yes" else 1,
        )
        hotwaterheating = st.selectbox(
            "Hot Water Heating",
            ["yes", "no"],
            index=0 if parsed_inputs.get("hotwaterheating") == "yes" else 1,
        )
    with a3:
        airconditioning = st.selectbox(
            "Air Conditioning",
            ["yes", "no"],
            index=0 if parsed_inputs.get("airconditioning") == "yes" else 1,
        )
        prefarea = st.selectbox(
            "Preferred Area",
            ["yes", "no"],
            index=0 if parsed_inputs.get("prefarea") == "yes" else 1,
            help="Located in a preferred/premium locality?",
        )

    st.markdown("##### 🅿️ Parking & Furnishing")
    p1, p2 = st.columns(2)
    with p1:
        parking = st.number_input(
            "Parking Spaces",
            min_value=0,
            max_value=5,
            value=parsed_inputs.get("parking", 2),
        )
    with p2:
        furnishingstatus = st.selectbox(
            "Furnishing Status",
            get_furnishing_options(label_encoders),
            index=(
                get_furnishing_options(label_encoders).index(parsed_inputs["furnishingstatus"])
                if parsed_inputs.get("furnishingstatus") in get_furnishing_options(label_encoders)
                else 0
            ),
        )

    submitted = st.form_submit_button("🎯 Predict Price", use_container_width=True, type="primary")
    auto_submit = voice_has_all_fields and not st.session_state.get("voice_auto_submit_executed", False)
    if auto_submit:
        submitted = True
    elif voice_confirm:
        submitted = True

# -------------------------------------------------------------------------
# Prediction
# -------------------------------------------------------------------------

if submitted:
    with st.spinner("Running the model..."):
        time.sleep(0.4)  # brief, intentional pause so the loading state is perceivable
        features = HouseFeatures(
            area=area, bedrooms=bedrooms, bathrooms=bathrooms, stories=stories,
            mainroad=mainroad, guestroom=guestroom, basement=basement,
            hotwaterheating=hotwaterheating, airconditioning=airconditioning,
            parking=parking, prefarea=prefarea, furnishingstatus=furnishingstatus,
        )
        try:
            price = predict_price(model, label_encoders, features)
        except Exception as exc:  # noqa: BLE001
            st.error(f"❌ Prediction failed: {exc}")
            st.stop()

        record = add_record(
            inputs={
                "area": area, "bedrooms": bedrooms, "bathrooms": bathrooms, "stories": stories,
                "mainroad": mainroad, "guestroom": guestroom, "basement": basement,
                "hotwaterheating": hotwaterheating, "airconditioning": airconditioning,
                "parking": parking, "prefarea": prefarea, "furnishingstatus": furnishingstatus,
            },
            predicted_price=price,
        )
        st.session_state["last_prediction_id"] = record["id"]
        st.session_state["voice_auto_submit_executed"] = True

    st.balloons()
    render_price_panel(price, timestamp=record["timestamp"])
    st.success("Saved to your Prediction History. Visit **Reports** to download a PDF/CSV summary.")

render_footer()
