
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Index, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(String(100))

    origin: Mapped[str] = mapped_column(String(100))

    destination: Mapped[str] = mapped_column(String(100))


class Stop(Base):
    __tablename__ = "stops"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    route_id: Mapped[int] = mapped_column(
        ForeignKey("routes.id")
    )

    name: Mapped[str] = mapped_column(String(100))

    sequence: Mapped[int] = mapped_column(Integer)

    __table_args__ = (
        Index(
            "uq_route_stop_sequence",
            "route_id",
            "sequence",
            unique=True
        ),
    )


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    route_id: Mapped[int] = mapped_column(
        ForeignKey("routes.id")
    )

    bus_name: Mapped[str] = mapped_column(String(100))

    travel_date: Mapped[date] = mapped_column(Date)

class Seat(Base):
    __tablename__ = "seats"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    trip_id: Mapped[int] = mapped_column(
        ForeignKey("trips.id")
    )

    seat_number: Mapped[str] = mapped_column(String(10))

    __table_args__ = (
        Index(
            "uq_trip_seat_number",
            "trip_id",
            "seat_number",
            unique=True
        ),
    )


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    pnr: Mapped[str] = mapped_column(
        String(30),
        unique=True
    )

    trip_id: Mapped[int] = mapped_column(
        ForeignKey("trips.id")
    )

    seat_id: Mapped[int] = mapped_column(
        ForeignKey("seats.id")
    )

    passenger_name: Mapped[str] = mapped_column(String(100))

    passenger_email: Mapped[str] = mapped_column(String(150))

    passenger_phone: Mapped[str] = mapped_column(String(15))

    boarding_stop_id: Mapped[int] = mapped_column(
        ForeignKey("stops.id")
    )

    drop_stop_id: Mapped[int] = mapped_column(
        ForeignKey("stops.id")
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="CONFIRMED"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    __table_args__ = (
        Index(
            "uq_active_trip_seat",
            "trip_id",
            "seat_id",
            unique=True,
            sqlite_where=text("status = 'CONFIRMED'"),
            postgresql_where=text("status = 'CONFIRMED'")
        ),
    )