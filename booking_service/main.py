from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI(title="Booking Service - Павло Голубчак")

STUDENT_N = 18
TOUR_SERVICE_URL = "http://tour-service:8000"

class BookingRequest(BaseModel):
    tour_id: int
    customer_name: str
    people_count: int

BOOKINGS = []

@app.post("/bookings")
def create_booking(booking: BookingRequest):
    # Запит до Tour Service
    try:
        response = requests.get(f"{TOUR_SERVICE_URL}/tours/{booking.tour_id}")
        response.raise_for_status()
        tour_data = response.json()["data"]
    except:
        raise HTTPException(status_code=503, detail="Tour Service unavailable")

    if not tour_data["available"]:
        raise HTTPException(status_code=400, detail="Tour is not available")

    new_booking = {
        "booking_id": len(BOOKINGS) + 1,
        "tour_id": booking.tour_id,
        "tour_name": tour_data["name"],
        "customer_name": booking.customer_name,
        "people_count": booking.people_count,
        "total_price": tour_data["price"] * booking.people_count,
        "status": "Confirmed",
        "student_id": STUDENT_N
    }
    
    BOOKINGS.append(new_booking)
    return new_booking

@app.get("/bookings")
def get_all_bookings():
    return {"bookings": BOOKINGS, "student_id": STUDENT_N}