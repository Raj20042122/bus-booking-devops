def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_readiness(client):
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["database"] == "connected"


def test_get_routes(client):
    response = client.get("/routes")

    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_trips(client):
    response = client.get("/trips")

    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_seats(client):
    response = client.get("/trips/1/seats")

    assert response.status_code == 200
    assert len(response.json()) == 10

    for seat in response.json():
        assert seat["available"] is True


def test_create_booking(client):

    booking_data = {
        "trip_id": 1,
        "seat_id": 1,
        "passenger_name": "Raj Kumar",
        "passenger_email": "raj@example.com",
        "passenger_phone": "9876543210",
        "boarding_stop_id": 1,
        "drop_stop_id": 4
    }

    response = client.post("/bookings", json=booking_data)

    assert response.status_code == 201
    assert response.json()["pnr"].startswith("BUS-")
    assert response.json()["status"] == "CONFIRMED"


def test_duplicate_booking(client):

    booking_data = {
        "trip_id": 1,
        "seat_id": 1,
        "passenger_name": "Raj Kumar",
        "passenger_email": "raj@example.com",
        "passenger_phone": "9876543210",
        "boarding_stop_id": 1,
        "drop_stop_id": 4
    }

    first = client.post("/bookings", json=booking_data)

    second = client.post("/bookings", json=booking_data)

    assert first.status_code == 201
    assert second.status_code == 409


def test_cancel_booking(client):

    booking_data = {
        "trip_id": 1,
        "seat_id": 1,
        "passenger_name": "Raj Kumar",
        "passenger_email": "raj@example.com",
        "passenger_phone": "9876543210",
        "boarding_stop_id": 1,
        "drop_stop_id": 4
    }

    booking = client.post("/bookings", json=booking_data)

    pnr = booking.json()["pnr"]

    response = client.patch(f"/bookings/{pnr}/cancel")

    assert response.status_code == 200
    assert response.json()["status"] == "CANCELLED"


def test_cancelled_seat_can_be_booked_again(client):

    booking_data = {
        "trip_id": 1,
        "seat_id": 1,
        "passenger_name": "Raj Kumar",
        "passenger_email": "raj@example.com",
        "passenger_phone": "9876543210",
        "boarding_stop_id": 1,
        "drop_stop_id": 4
    }

    first = client.post("/bookings", json=booking_data)

    pnr = first.json()["pnr"]

    client.patch(f"/bookings/{pnr}/cancel")

    second = client.post("/bookings", json=booking_data)

    assert second.status_code == 201


def test_invalid_passenger_phone(client):

    booking_data = {
        "trip_id": 1,
        "seat_id": 1,
        "passenger_name": "Raj Kumar",
        "passenger_email": "raj@example.com",
        "passenger_phone": "123",
        "boarding_stop_id": 1,
        "drop_stop_id": 4
    }

    response = client.post("/bookings", json=booking_data)

    assert response.status_code == 422


def test_invalid_boarding_drop_order(client):

    booking_data = {
        "trip_id": 1,
        "seat_id": 1,
        "passenger_name": "Raj Kumar",
        "passenger_email": "raj@example.com",
        "passenger_phone": "9876543210",
        "boarding_stop_id": 4,
        "drop_stop_id": 1
    }

    response = client.post("/bookings", json=booking_data)

    assert response.status_code == 400