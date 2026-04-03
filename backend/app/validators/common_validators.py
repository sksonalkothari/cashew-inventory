from datetime import datetime

from pydantic import model_validator

def not_empty(value: str, field_name: str):
    if not value.strip():
        raise ValueError(f"{field_name.capitalize()} cannot be empty")
    return value

def must_be_in(value: str, allowed: set, field_name: str):
    if value not in allowed:
        raise ValueError(f"{field_name.capitalize()} must be one of {', '.join(sorted(allowed))}")
    return value

def valid_date(value: str, field_name: str):
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"{field_name.capitalize()} must be in YYYY-MM-DD format")
    return value

def positive_float(value: float, field_name: str):
    if value <= 0:
        raise ValueError(f"{field_name.replace('_', ' ').capitalize()} must be greater than zero")
    return value

def positive_int(value: int, field_name: str):
    if value <= 0:
        raise ValueError(f"{field_name.replace('_', ' ').capitalize()} must be greater than zero")
    return value

def remap_date_field(target: str):
    def _remap(cls, values):
        if "date" in values:
            values[target] = values["date"]
        return values
    return model_validator(mode="before")(_remap)