from datetime import date
from pydantic import BaseModel, ConfigDict, Field, field_validator
import re


class RouteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    origin: str
    destination: str


class TripResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    route_id: int
    bus_name: str
    travel_date: date


class SeatResponse(BaseModel):
    id: int
    seat_number: str
    available: bool


class BookingCreate(BaseModel):
    trip_id: int
    seat_id: int
    passenger_name: str = Field(min_length=2, max_length=100)
    passenger_email: str
    passenger_phone: str = Field(pattern=r"^\d{10,15}$")
    boarding_stop_id: int
    drop_stop_id: int

    @field_validator("passenger_email")
    @classmethod
    def validate_email(cls, value):
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            raise ValueError("Invalid email address")

        return value

    @field_validator("passenger_name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Passenger name cannot be empty")

        return value


class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pnr: str
    trip_id: int
    seat_id: int
    passenger_name: str
    passenger_email: str
    passenger_phone: str
    boarding_stop_id: int
    drop_stop_id: int
    status: str