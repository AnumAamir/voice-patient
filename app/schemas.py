from datetime import date
from typing import Literal
import re

from pydantic import BaseModel, field_validator
class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    sex: Literal["Male", "Female", "Other", "Decline to Answer"]
    phone_number: str
    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value):
        digits = "".join(filter(str.isdigit, value))

        if len(digits) != 10:
            raise ValueError("Phone number must contain exactly 10 digits")

        return digits
    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, value):
        if value > date.today():
            raise ValueError("Date of birth cannot be in the future")

        return value
    @field_validator("state")
    @classmethod
    def validate_state(cls, value):
        value = value.strip().upper()

        if not re.fullmatch(r"[A-Z]{2}", value):
            raise ValueError("State must be exactly 2 letters")

        return value


    @field_validator("zip_code")
    @classmethod
    def validate_zip_code(cls, value):
        value = value.strip()

        if not re.fullmatch(r"\d{5}(-\d{4})?", value):
            raise ValueError("ZIP code must be 5 digits or ZIP+4")

        return value
    @field_validator(
        "first_name",
        "last_name",
        "address_line_1",
        "city"
    )
    @classmethod
    def validate_required_text(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty")

        return value
    address_line_1: str
    address_line_2: str | None = None
    city: str
    state: str
    zip_code: str
    email: str | None = None
    insurance_provider: str | None = None
    insurance_member_id: str | None = None
    preferred_language: str = "English"
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None

class PatientUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: date | None = None
    sex: Literal["Male", "Female", "Other", "Decline to Answer"] | None = None
    phone_number: str | None = None
    address_line_1: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    email: str | None = None
    insurance_provider: str | None = None
    insurance_member_id: str | None = None
    preferred_language: str | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None

    @field_validator("phone_number", "emergency_contact_phone")
    @classmethod
    def validate_phone_number(cls, value):
        if value is None:
            return value

        digits = "".join(filter(str.isdigit, value))

        if len(digits) != 10:
            raise ValueError("Phone number must contain exactly 10 digits")

        return digits

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, value):
        if value is None:
            return value

        if value > date.today():
            raise ValueError("Date of birth cannot be in the future")

        return value

    @field_validator("state")
    @classmethod
    def validate_state(cls, value):
        if value is None:
            return value

        value = value.strip().upper()

        if not re.fullmatch(r"[A-Z]{2}", value):
            raise ValueError("State must be exactly 2 letters")

        return value

    @field_validator("zip_code")
    @classmethod
    def validate_zip_code(cls, value):
        if value is None:
            return value

        value = value.strip()

        if not re.fullmatch(r"\d{5}(-\d{4})?", value):
            raise ValueError("ZIP code must be 5 digits or ZIP+4")

        return value