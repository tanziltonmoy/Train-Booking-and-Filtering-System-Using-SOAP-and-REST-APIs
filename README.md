# 🚆 Train Booking & Filtering System (SOAP & REST)

## **Overview**
This project implements a **Train Booking Web Service (SOAP)** and a **Train Filtering REST API**, enabling seamless communication between SOAP and REST services.

## **System Architecture**
- **SOAP Service (A)**: Handles **train search, booking, and reservation management**.
- **REST Service (B)**: Handles **train filtering, availability updates, and reservations**.
- **Database**: Stores train schedules, seats, and reservation details.

## **🔧 Technologies Used**
- **FastAPI** (REST API)
- **Spyne** (SOAP API)
- **SQLite** (Database)
- **SQLAlchemy** (ORM)
- **Postman & Curl** (API Testing)

---
## **📌 Features**
### **SOAP Web Service (A)**
| Feature          | Endpoint | Description |
|----------------|----------|--------------|
| **Train Search** | `search_trains` | Calls REST `/trains/filter` to fetch train availability. |
| **Book Tickets** | `book_tickets` | Calls REST `/reservations` to book tickets. |
| **Cancel Reservation** | `cancel_reservation` | Calls REST `/reservations/cancel` to cancel a reservation. |

### **REST Web Service (B)**
| Feature          | Endpoint | Description |
|----------------|----------|--------------|
| **Train Filtering** | `/trains/filter` | Returns available trains based on user criteria. |
| **Train Reservation** | `/reservations` | Reserves seats for a train. |
| **Cancel Reservation** | `/reservations/cancel` | Cancels a train reservation. |

---
## **🚀 How to Run the Services**
### **1️⃣ Start the REST API (B)**
```sh
 python -m services.rest.main
```

### **2️⃣ Start the SOAP Service (A)**
```sh
python -m services.soap.main
```

---
## **📝 API Usage & Testing**
### **🔹 Train Search (SOAP -> REST)**
📌 **SOAP Request:**
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:train="train.booking.soap">
    <soapenv:Body>
        <train:search_trains>
            <train:departure_station>Paris</train:departure_station>
            <train:arrival_station>Lyon</train:arrival_station>
            <train:outbound_date>2025-02-01T08:00:00</train:outbound_date>
            <train:seat_class>Standard</train:seat_class>
        </train:search_trains>
    </soapenv:Body>
</soapenv:Envelope>
```
✔️ **Expected Response:**
```json
[
    {
        "train_id": 1,
        "departure_station": "Paris",
        "arrival_station": "Lyon",
        "available_seats": 5
    }
]
```

---
### **🔹 Book Train Tickets (SOAP -> REST)**
📌 **SOAP Request:**
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:train="train.booking.soap">
    <soapenv:Body>
        <train:book_tickets>
            <train:train_id>1</train:train_id>
            <train:seat_class>Standard</train:seat_class>
            <train:num_tickets>2</train:num_tickets>
            <train:client_id>1001</train:client_id>
        </train:book_tickets>
    </soapenv:Body>
</soapenv:Envelope>
```
✔️ **Expected Response:**
```xml
<soapenv:Envelope>
    <soapenv:Body>
        <train:book_ticketsResponse>
            <train:return>Reservation successful.</train:return>
        </train:book_ticketsResponse>
    </soapenv:Body>
</soapenv:Envelope>
```

---
### **🔹 Cancel Reservation (SOAP -> REST)**
📌 **SOAP Request:**
```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:train="train.booking.soap">
    <soapenv:Body>
        <train:cancel_reservation>
            <train:reservation_id>5</train:reservation_id>
        </train:cancel_reservation>
    </soapenv:Body>
</soapenv:Envelope>
```
✔️ **Expected Response:**
```xml
<soapenv:Envelope>
    <soapenv:Body>
        <train:cancel_reservationResponse>
            <train:return>Reservation 5 successfully canceled.</train:return>
        </train:cancel_reservationResponse>
    </soapenv:Body>
</soapenv:Envelope>
```

---
## **📜 API Documentation (Swagger / OpenAPI)**
Run the REST API and open **Swagger UI** at:
```
http://127.0.0.1:8000/docs
```

---
## **✅ Testing with Postman**
### **REST API Test (Train Search)**
- **GET** `http://127.0.0.1:8000/trains/filter?departure_station=Paris&arrival_station=Lyon&outbound_date=2025-02-01T08:00:00`
- **Expected Response:** List of available trains

### **SOAP API Test (Book Ticket)**
- Send SOAP request in **Postman** under `http://127.0.0.1:8001`
- **Expected Response:** Reservation successful

---
## **📌 Next Steps**
- Improve logging and error handling
- Add authentication & user sessions
- Optimize SOAP-REST communication

---
## **📜 License**
This project is licensed under the MIT License.

---
### **👨‍💻 Developed by Tanzil Al Sabah** 🚀

