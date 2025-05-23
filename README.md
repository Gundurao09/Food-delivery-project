#  Food-delivery API

A FastAPI-based RESTful API for managing food delivery orders with features like status tracking, cancellation reasons, and summary insights. This service uses an in-memory data store and includes thread-safety for concurrent access.

##  Features

- Create new orders
- View list of all orders
- Get order details by ID
- Update order status (including cancellation with reason)
- View summary statistics (total orders and total amount)
- Thread-safe in-memory order storage (no database required)

##  Setup Instructions

### 1. Clone the repository

- git clone [(https://github.com/Gundurao09/Food-delivery/)]

### 2. Create and activate a virtual environment

- python -m venv venv
- macOS/Linux: source venv/bin/activate
- Windows: venv\Scripts\activate

### 3. Install required packages

- pip install -r requirements.txt

##### If you don’t have a requirements.txt file, create one with the following content:

- fastapi
- uvicorn
- pydantic

##  Running the API Server

- uvicorn main:app --reload

* Replace main with your Python filename (without .py)
* The --reload option automatically restarts the server on code changes.

##  API Endpoints Overview

- POST /orders/ — Create a new order
- GET /orders/ — List all orders
- GET /orders/{order_id} — Get order details
- PUT /orders/{order_id} — Update order status
- GET /orders/summary — Get summary statistics

##  Future Improvements (Optional)

- Data is stored only in-memory and will reset on server restart.
- Adding persistent storage like a database (SQLite, PostgreSQL) would improve durability.
- Authentication & authorization not implemented yet.
- More detailed validation and error handling can be added.
