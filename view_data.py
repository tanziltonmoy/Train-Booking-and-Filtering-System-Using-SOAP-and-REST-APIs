from sqlalchemy.orm import Session
from database.database import SessionLocal
from database.models import Train, Seat

def view_data():
    db: Session = SessionLocal()
    try:
        # Fetch train data
        print("Trains:")
        trains = db.query(Train).all()
        for train in trains:
            print(
                f"ID: {train.train_id}, From: {train.departure_station}, To: {train.arrival_station}, "
                f"Departure: {train.departure_datetime}, Arrival: {train.arrival_datetime}"
            )

        # Fetch seat data
        print("\nSeats:")
        seats = db.query(Seat).all()
        for seat in seats:
            print(
                f"Seat ID: {seat.seat_id}, Train ID: {seat.train_id}, Class: {seat.seat_class}, "
                f"Status: {seat.status}, Fare: {seat.fare}"
            )
    finally:
        db.close()

if __name__ == "__main__":
    view_data()
