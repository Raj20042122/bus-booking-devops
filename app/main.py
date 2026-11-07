from fastapi import FastAPI

app = FastAPI(
    title="Bus Booking API",
    description="Trip and seat reservation service",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Bus Booking API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }