import requests
from concurrent.futures import ThreadPoolExecutor

url = "http://13.239.41.176/bookings"

booking = {
    "trip_id": 1,
    "seat_id": 4,
    "passenger_name": "Concurrent Test",
    "passenger_email": "concurrent@example.com",
    "passenger_phone": "9876543210",
    "boarding_stop_id": 1,
    "drop_stop_id": 4
}

def book():
    try:
        response = requests.post(url, json=booking, timeout=20)
        return response.status_code, response.text
    except Exception as error:
        return "ERROR", str(error)

with ThreadPoolExecutor(max_workers=2) as executor:
    results = list(executor.map(lambda _: book(), range(2)))

for result in results:
    print(result)
