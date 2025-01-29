from pydantic import BaseModel

class TrainFilterResponse(BaseModel):
    train_id: int
    departure_station: str
    arrival_station: str
    available_seats: int

class ReservationRequest(BaseModel):
    train_id: int
    seat_class: str
    num_tickets: int
    client_id: int  # Added to match updated REST API

class CancelReservationRequest(BaseModel):
    reservation_id: int
