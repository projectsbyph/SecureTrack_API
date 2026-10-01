from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import config

app = FastAPI(title="SecureTrack API", description="API for SecureTrack application", version="1.0.0")

# Simple "database" in memory for demonstration purposes (get deleted on restart)
bookings_db = {
    "TRAIN-12345": {
        "train_number": "12345",
        "name": "Person1",
        "origin": "Stockholm",
        "destination": "Copenhagen",
        "departure_time": "2023-10-01 08:00:00",
        "arrival_time": "2023-10-01 16:00:00",
        "card_number": "4111111111111111",
        "status": "confirmed"
    }
}

class BookingRequest(BaseModel):
    train_number: str
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    card_number: str

@app.get("/")
def root():
    return {"message": "Welcome to the SecureTrack API!"}

@app.get("/routes")
def get_routes():
    # For demonstration, returning a static list of routes, in a real application this would query a database or external service
    return {
        "routes": [
            {"train_number": "12345", "origin": "Stockholm", "destination": "Copenhagen"},
            {"train_number": "67890", "origin": "Oslo", "destination": "Bergen"},
            {"train_number": "54321", "origin": "Helsinki", "destination": "Turku"}
        ]
    }

@app.post("/bookings")
def create_booking(booking_request: BookingRequest):
    # Simulate booking creation and payment processing
    booking_id = f"TRAIN-{booking_request.train_number}"
    if booking_id in bookings_db:
        raise HTTPException(status_code=400, detail="Booking already exists.")

    # Simulate payment processing using the fake API key and token from config.py
    if (config.TRANSPORTCOMPANTY_API_KEY != "live_key_928374982374_fake_key_for_testing" or 
        config.PAYMENT_GATEWAY_TOKEN != "sk_live_51HXXXXX_fake_stripe_token_for_scanning"):
        raise HTTPException(status_code=500, detail="Invalid API credentials.")

    # If we reach here, the booking is valid and payment is processed
    bookings_db[booking_id] = {
        "train_number": booking_request.train_number,
        "name": booking_request.name,
        "origin": booking_request.origin,
        "destination": booking_request.destination,
        "departure_time": booking_request.departure_time,
        "arrival_time": booking_request.arrival_time,
        "card_number": booking_request.card_number,
        "status": "confirmed"
    }

    return {"message": "Booking created successfully.", "booking_id": booking_id}   

@app.get("/bookings/{booking_id}")
def get_booking(booking_id: str):
    booking = bookings_db.get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found.")
    return booking
