from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Train(Base):
    __tablename__ = "trains"
    __table_args__ = (Index("idx_departure_arrival", "departure_station", "arrival_station"),)

    train_id = Column(Integer, primary_key=True, autoincrement=True)
    departure_station = Column(String(50), nullable=False)
    arrival_station = Column(String(50), nullable=False)
    departure_datetime = Column(DateTime, nullable=False)
    arrival_datetime = Column(DateTime, nullable=False)

    seats = relationship("Seat", back_populates="train")


class Seat(Base):
    __tablename__ = "seats"

    seat_id = Column(Integer, primary_key=True, autoincrement=True)
    train_id = Column(Integer, ForeignKey("trains.train_id"), nullable=False)
    seat_class = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="Available")
    fare = Column(Float, nullable=False)

    train = relationship("Train", back_populates="seats")
    reservation = relationship("Reservation", back_populates="seat", uselist=False)


class Client(Base):
    __tablename__ = "clients"

    client_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # Store hashed passwords

    reservations = relationship("Reservation", back_populates="client")


class Reservation(Base):
    __tablename__ = "reservations"

    reservation_id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.seat_id"), nullable=False)
    ticket_type = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="Confirmed")
    cancellation_reason = Column(String(255), nullable=True)  # New Column for tracking cancellation reason

    client = relationship("Client", back_populates="reservations")
    seat = relationship("Seat", back_populates="reservation")
