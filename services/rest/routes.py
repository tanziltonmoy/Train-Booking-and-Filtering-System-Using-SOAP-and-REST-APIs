from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from database.database import get_db
from database.models import Train, Seat, Reservation
from datetime import datetime

router = APIRouter()

# Request model for making a reservation
class ReservationRequest(BaseModel):
    train_id: int
    seat_class: str
    num_tickets: int
    client_id: int  # Added client_id field for real authentication

# Request model for canceling a reservation
class CancelReservationRequest(BaseModel):
    reservation_id: int


@router.get("/trains/filter")
def filter_trains(
    departure_station: str = Query(..., description="Station where the train departs from."),
    arrival_station: str = Query(..., description="Station where the train arrives."),
    outbound_date: datetime = Query(..., description="Departure date and time."),
    return_date: Optional[datetime] = Query(None, description="Return date for round trips."),
    seat_class: Optional[str] = Query(None, description="Class of seat (e.g., First, Business, Standard)."),
    db: Session = Depends(get_db),
):
    """
    Filters trains based on the departure station, arrival station, and other criteria.
    """
    query = db.query(Train).filter(
        Train.departure_station == departure_station,
        Train.arrival_station == arrival_station,
        Train.departure_datetime >= outbound_date
    )

    if return_date:
        query = query.filter(Train.departure_datetime <= return_date)

    trains = query.all()
    if not trains:
        raise HTTPException(status_code=404, detail="No trains available.")

    response = []
    for train in trains:
        seat_query = db.query(Seat).filter(
            Seat.train_id == train.train_id,
            Seat.status == "Available"
        )

        if seat_class:
            seat_query = seat_query.filter(Seat.seat_class == seat_class)

        available_seats = seat_query.count()

        response.append({
            "train_id": train.train_id,
            "departure_station": train.departure_station,
            "arrival_station": train.arrival_station,
            "available_seats": available_seats,
        })

    return response


@router.post("/reservations")
def update_reservation(request: ReservationRequest, db: Session = Depends(get_db)):
    """
    Reserves seats for a specified train and seat class.
    """
    # Check seat availability
    seats = db.query(Seat).filter(
        Seat.train_id == request.train_id,
        Seat.seat_class == request.seat_class,
        Seat.status == "Available"
    ).limit(request.num_tickets).all()

    if len(seats) < request.num_tickets:
        raise HTTPException(status_code=400, detail="Not enough available seats.")

    # Reserve seats
    reserved_seat_ids = []
    for seat in seats:
        seat.status = "Reserved"
        db.add(seat)
        reserved_seat_ids.append(seat.seat_id)
    db.commit()

    # Add reservation to the reservations table
    for seat_id in reserved_seat_ids:
        reservation = Reservation(
            client_id=request.client_id,  # Now using a real client_id
            seat_id=seat_id,
            ticket_type="Flexible",  # Example ticket type, adjust as needed
            status="Confirmed"
        )
        db.add(reservation)
    db.commit()

    return {
        "message": f"Successfully reserved {request.num_tickets} {request.seat_class} seat(s) on train {request.train_id}.",
        "reserved_seat_ids": reserved_seat_ids,
    }



@router.post("/reservations/cancel")
def cancel_reservation(request: CancelReservationRequest, db: Session = Depends(get_db)):
    """
    Cancel a reservation based on the reservation ID.
    """
    # Check if the reservation exists
    reservation = db.query(Reservation).filter(Reservation.reservation_id == request.reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found.")

    # Update the seat status to 'Available'
    seat = db.query(Seat).filter(Seat.seat_id == reservation.seat_id).first()
    if seat:
        seat.status = "Available"
        db.add(seat)

    # Instead of deleting the reservation, mark it as "Canceled"
    reservation.status = "Canceled"
    db.add(reservation)

    db.commit()

    return {"message": f"Reservation with ID {request.reservation_id} has been successfully canceled."}
