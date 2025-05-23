from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import threading

app = FastAPI(title="Order Management API")

order_id_seq = 1
db_lock = threading.Lock()

class Order(BaseModel):
    order_id: int
    description: str
    status: str
    amount: float
    cancellation_reasons: List[str] = Field(default_factory=list)

orders_db: Dict[int, Order] = {}

class OrderStatusUpdate(BaseModel):
    status: str
    cancellation_reason: Optional[str] = None

VALID_STATUSES = ["Pending", "Successful", "Cancelled"]

@app.post("/orders/", response_model=Order, summary="Create a new order")
def create_order(order: Order):
    global order_id_seq
    with db_lock:
        order.order_id = order_id_seq
        if order.status not in VALID_STATUSES:
            raise HTTPException(status_code=400, detail="Invalid status value.")
        orders_db[order_id_seq] = order
        order_id_seq += 1
    return order

@app.get("/orders/", response_model=List[Order], summary="Get list of all orders")
def list_orders():
    return list(orders_db.values())

@app.get("/orders/summary", summary="Get summary statistics of orders")
def get_order_summary():
    total_orders = len(orders_db)
    total_amount = sum(order.amount for order in orders_db.values())
    return {
        "total_orders": total_orders,
        "total_amount": total_amount
    }

@app.get("/orders/{order_id}", response_model=Order, summary="Get details of a specific order")
def get_order(order_id: int):
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}", response_model=Order, summary="Update the status of an existing order")
def update_order_status(order_id: int, update: OrderStatusUpdate):
    if update.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid status value.")

    with db_lock:
        order = orders_db.get(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        current_status = order.status

        # Logic for status transitions
        if current_status == "Successful":
            raise HTTPException(status_code=400, detail="Order is already successful and cannot be updated.")

        if current_status == "Cancelled":
            raise HTTPException(status_code=400, detail="Order is already cancelled. Please create a new order.")

        if current_status == "Pending":
            if update.status == "Cancelled":
                reason = update.cancellation_reason or "No reason provided"
                order.cancellation_reasons.append(reason)
                order.status = "Cancelled"
            elif update.status == "Successful":
                order.status = "Successful"
            else:
                raise HTTPException(status_code=400, detail="Invalid status update from Pending.")
        
        return order 