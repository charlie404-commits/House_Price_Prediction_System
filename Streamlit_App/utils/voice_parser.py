"""
utils/voice_parser.py
---------------------
Parses simple natural language property descriptions into the
model's structured input fields.
"""

from __future__ import annotations

import re
from typing import Any, Dict

NUMBERS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
}

FURNISHING_MAP = {
    "fully furnished": "furnished",
    "furnished": "furnished",
    "semi furnished": "semi-furnished",
    "semi-furnished": "semi-furnished",
    "unfurnished": "unfurnished",
}

BOOLEAN_FEATURES = {
    "mainroad": ["main road", "mainroad"],
    "guestroom": ["guest room", "guestroom"],
    "basement": ["basement"],
    "hotwaterheating": ["hot water heating", "hot water", "hot water heater"],
    "airconditioning": ["air conditioning", "air conditioner", "ac"],
    "prefarea": ["preferred area", "preferred locality", "premium location", "prime area"],
}

NUMBER_WORD_PATTERN = r"(?:\d{1,5}|" + "|".join(NUMBERS.keys()) + r")"


def _text_to_number(value: str) -> int | None:
    value = value.strip().lower().replace(" ", "")
    if value.isdigit():
        return int(value)
    return NUMBERS.get(value)


def _find_numeric(command: str, keys: tuple[str, ...]) -> int | None:
    value_pattern = NUMBER_WORD_PATTERN
    for key in keys:
        patterns = [
            rf"(?:{key})\s*(?:is|are|=|:)?\s*({value_pattern})",
            rf"({value_pattern})\s*(?:{key})",
        ]
        for pattern in patterns:
            match = re.search(pattern, command)
            if match:
                return _text_to_number(match.group(1))
    return None


def _find_boolean(command: str, phrases: list[str]) -> str | None:
    text = command.lower()
    for phrase in phrases:
        if f"no {phrase}" in text or f"not {phrase}" in text or f"without {phrase}" in text:
            return "no"
        if phrase in text:
            return "yes"
    return None


def _find_furnishing(command: str) -> str | None:
    for phrase, mapped in FURNISHING_MAP.items():
        if phrase in command:
            return mapped
    return None


def parse_voice_command(command: str) -> Dict[str, Any]:
    """Return a partial input dictionary parsed from natural language."""
    result: Dict[str, Any] = {}
    text = command.lower()

    area = _find_numeric(text, ("area", "size", "sq ft", "square feet", "square foot", "square meter", "sq meters"))
    if area is not None:
        result["area"] = area

    bedrooms = _find_numeric(text, ("bedrooms", "beds", "bedroom"))
    if bedrooms is not None:
        result["bedrooms"] = bedrooms

    bathrooms = _find_numeric(text, ("bathrooms", "baths", "bathroom"))
    if bathrooms is not None:
        result["bathrooms"] = bathrooms

    stories = _find_numeric(text, ("stories", "floors", "storeys", "storey"))
    if stories is not None:
        result["stories"] = stories

    parking = _find_numeric(text, ("parking", "car park", "cars", "parking spaces", "parking space"))
    if parking is not None:
        result["parking"] = parking

    for key, phrases in BOOLEAN_FEATURES.items():
        boolean_value = _find_boolean(text, phrases)
        if boolean_value is not None:
            result[key] = boolean_value

    furnishingstatus = _find_furnishing(text)
    if furnishingstatus is not None:
        result["furnishingstatus"] = furnishingstatus

    return result
