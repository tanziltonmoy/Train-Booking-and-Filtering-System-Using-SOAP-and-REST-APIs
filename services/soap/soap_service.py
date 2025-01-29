from spyne import Application, rpc, ServiceBase, Unicode, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrainBookingService(ServiceBase):
    @rpc(Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def search_trains(ctx, departure_station, arrival_station, outbound_date, seat_class):
        """
        Searches for trains based on the provided parameters by interacting with the REST API.
        """
        url = "http://127.0.0.1:8000/trains/filter"
        params = {
            "departure_station": departure_station,
            "arrival_station": arrival_station,
            "outbound_date": outbound_date,
            "seat_class": seat_class
        }

        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                # Parse and format the REST API response
                trains = response.json()
                if not trains:
                    return "No trains available."
                return json.dumps(trains, indent=2)
            elif response.status_code == 404:
                return "No trains available."
            else:
                return f"Failed to fetch trains. REST API responded with: {response.text}"
        except Exception as e:
            logger.error(f"Error during search_trains: {str(e)}")
            return f"Error occurred while searching for trains: {str(e)}"

    @rpc(Integer, Unicode, Integer, Integer, _returns=Unicode)
    def book_tickets(ctx, train_id, seat_class, num_tickets, client_id):
        """
        Books tickets by interacting with the REST API.
        """
        url = "http://127.0.0.1:8000/reservations"
        payload = {
            "train_id": train_id,
            "seat_class": seat_class,
            "num_tickets": num_tickets,
            "client_id": client_id  # New field to align with updated REST API
        }
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return "Reservation successful."
            elif response.status_code == 400:
                return f"Reservation failed: {response.json().get('detail', 'Unknown error')}"
            else:
                return f"Reservation failed. REST API responded with: {response.text}"
        except Exception as e:
            logger.error(f"Error during book_tickets: {str(e)}")
            return f"Error occurred while booking tickets: {str(e)}"

    @rpc(Integer, _returns=Unicode)
    def cancel_reservation(ctx, reservation_id):
        """
        Cancels a reservation via the REST API.
        """
        url = "http://127.0.0.1:8000/reservations/cancel"
        payload = {"reservation_id": reservation_id}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return f"Reservation {reservation_id} successfully canceled."
            elif response.status_code == 404:
                return f"Cancellation failed: Reservation {reservation_id} not found."
            else:
                return f"Cancellation failed. REST API responded with: {response.text}"
        except Exception as e:
            logger.error(f"Error during cancel_reservation: {str(e)}")
            return f"Error occurred while canceling reservation: {str(e)}"


# Spyne Application
application = Application(
    [TrainBookingService],
    tns="train.booking.soap",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

