import uuid

from datetime import date, timedelta

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import Base, engine, get_db
from app.models import Route, Stop, Trip, Seat, Booking
from app.schemas import (
    RouteResponse,
    TripResponse,
    SeatResponse,
    BookingCreate,
    BookingResponse
)

app = FastAPI(
    title="Bus Booking API",
    description="Trip and seat reservation service",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

    db = next(get_db())

    try:
        if db.scalar(select(Route.id).limit(1)) is None:

            route = Route(
                name="Delhi to Chandigarh",
                origin="Delhi",
                destination="Chandigarh"
            )

            db.add(route)
            db.flush()

            stops = [
                Stop(route_id=route.id, name="Delhi ISBT", sequence=1),
                Stop(route_id=route.id, name="Panipat", sequence=2),
                Stop(route_id=route.id, name="Ambala", sequence=3),
                Stop(route_id=route.id, name="Chandigarh", sequence=4)
            ]

            db.add_all(stops)
            db.flush()

            trip = Trip(
                route_id=route.id,
                bus_name="Express Travels",
                travel_date=date.today() + timedelta(days=2)
            )

            db.add(trip)
            db.flush()

            seats = [
                Seat(trip_id=trip.id, seat_number=f"A{i}")
                for i in range(1, 11)
            ]

            db.add_all(seats)
            db.commit()

    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "Welcome to Bus Booking API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/ready")
def readiness(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )


@app.get("/routes", response_model=list[RouteResponse])
def get_routes(db: Session = Depends(get_db)):
    return db.scalars(select(Route)).all()


@app.get("/trips", response_model=list[TripResponse])
def get_trips(
    route_id: int | None = None,
    travel_date: date | None = None,
    db: Session = Depends(get_db)
):
    query = select(Trip)

    if route_id is not None:
        query = query.where(Trip.route_id == route_id)

    if travel_date is not None:
        query = query.where(Trip.travel_date == travel_date)

    return db.scalars(query).all()


@app.get(
    "/trips/{trip_id}/seats",
    response_model=list[SeatResponse]
)
def get_seats(
    trip_id: int,
    db: Session = Depends(get_db)
):
    trip = db.get(Trip, trip_id)

    if not trip:
        raise HTTPException(404, "Trip not found")

    seats = db.scalars(
        select(Seat).where(Seat.trip_id == trip_id)
    ).all()

    booked_ids = set(
        db.scalars(
            select(Booking.seat_id).where(
                Booking.trip_id == trip_id,
                Booking.status == "CONFIRMED"
            )
        ).all()
    )

    return [
        {
            "id": seat.id,
            "seat_number": seat.seat_number,
            "available": seat.id not in booked_ids
        }
        for seat in seats
    ]


@app.post(
    "/bookings",
    response_model=BookingResponse,
    status_code=201
)
def create_booking(
    data: BookingCreate,
    db: Session = Depends(get_db)
):
    trip = db.get(Trip, data.trip_id)

    if not trip:
        raise HTTPException(404, "Trip not found")

    if trip.travel_date < date.today():
        raise HTTPException(400, "Travel date has passed")

    seat = db.get(Seat, data.seat_id)

    if not seat or seat.trip_id != trip.id:
        raise HTTPException(400, "Invalid seat for this trip")

    boarding = db.get(Stop, data.boarding_stop_id)
    dropping = db.get(Stop, data.drop_stop_id)

    if (
        not boarding
        or not dropping
        or boarding.route_id != trip.route_id
        or dropping.route_id != trip.route_id
    ):
        raise HTTPException(400, "Invalid boarding or drop stop")

    if boarding.sequence >= dropping.sequence:
        raise HTTPException(
            400,
            "Boarding stop must come before drop stop"
        )

    booking = Booking(
        pnr="BUS-" + uuid.uuid4().hex[:10].upper(),
        trip_id=trip.id,
        seat_id=seat.id,
        passenger_name=data.passenger_name,
        passenger_email=data.passenger_email,
        passenger_phone=data.passenger_phone,
        boarding_stop_id=boarding.id,
        drop_stop_id=dropping.id,
        status="CONFIRMED"
    )

    db.add(booking)

    try:
        db.commit()
        db.refresh(booking)
        return booking

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Seat already booked for this trip"
        )


@app.get(
    "/bookings/{pnr}",
    response_model=BookingResponse
)
def get_booking(
    pnr: str,
    db: Session = Depends(get_db)
):
    booking = db.scalar(
        select(Booking).where(Booking.pnr == pnr)
    )

    if not booking:
        raise HTTPException(404, "Booking not found")

    return booking


@app.patch(
    "/bookings/{pnr}/cancel",
    response_model=BookingResponse
)
def cancel_booking(
    pnr: str,
    db: Session = Depends(get_db)
):
    booking = db.scalar(
        select(Booking).where(Booking.pnr == pnr)
    )

    if not booking:
        raise HTTPException(404, "Booking not found")

    if booking.status == "CANCELLED":
        raise HTTPException(400, "Booking already cancelled")

    booking.status = "CANCELLED"
    db.commit()
    db.refresh(booking)

    return booking