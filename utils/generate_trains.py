import sys
import os
from sqlalchemy.orm import Session
from database.database import SessionLocal
from database.models import Train, Seat
from datetime import datetime, timedelta
import random

# Ensure the root directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def generate_random_trains_and_seats(db: Session, num_trains: int = 50):
    stations = ["Paris", "Lyon", "Marseille", "Nice"]
    seat_classes = ["First", "Business", "Standard"]

    for _ in range(num_trains):
        departure_station, arrival_station = random.sample(stations, 2)
        departure_datetime = datetime.now() + timedelta(days=random.randint(1, 30))
        arrival_datetime = departure_datetime + timedelta(hours=random.randint(1, 5))

        train = Train(
            departure_station=departure_station,
            arrival_station=arrival_station,
            departure_datetime=departure_datetime,
            arrival_datetime=arrival_datetime,
        )
        db.add(train)
        db.commit()

        # Ensure a minimum number of available seats to avoid errors
        min_seats = 10  
        max_seats = 50  

        for _ in range(random.randint(min_seats, max_seats)):
            seat = Seat(
                train_id=train.train_id,
                seat_class=random.choice(seat_classes),
                status="Available",  # Make sure seats start as available
                fare=random.uniform(50, 300),
            )
            db.add(seat)

        db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    try:
        generate_random_trains_and_seats(db, num_trains=50)
        print("Train data generated successfully!")
    finally:
        db.close()
