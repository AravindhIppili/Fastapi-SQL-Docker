import asyncio
import traceback
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from Routes.router import router
from Utils.DAL.connector import MySQLBase
from Utils.DAL.models import Orders, Pizzas, PizzaTopping
from Utils.pydantic_models import *


async def update_order_status(db: Session, order_id: str):
    try:
        print(f"Update order status for {order_id}")
        await asyncio.sleep(60)
        db_order = db.query(Orders).filter_by(order_id=order_id).first()

        if db_order.status.value == IOrderStatus.PLACED.value:
            db_order.status = IOrderStatus.ACCEPTED.value
            print(f"Order - {order_id} status updated to ACCEPTED")
            db.commit()

        await asyncio.sleep(60)
        if db_order.status.value == IOrderStatus.ACCEPTED.value:
            db_order.status = IOrderStatus.PREPARING.value
            db.commit()
            print(f"Order - {order_id} status updated to PREPARING")

        await asyncio.sleep(180)
        if db_order.status.value == IOrderStatus.PREPARING.value:
            db_order.status = IOrderStatus.DISPATCHED.value
            db.commit()
            print(f"Order - {order_id} status updated to DISPATCHED")

        await asyncio.sleep(300)
        if db_order.status.value == IOrderStatus.DISPATCHED.value:
            db_order.status = IOrderStatus.DELIVERED.value
            db.commit()
            print(f"Order - {order_id} status updated to DELIVERED")

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500, detail="Error updating order status"
        ) from e


@router.post("/order")
async def create_order(order: IOrder, db: Session = Depends(MySQLBase.get_session)):
    try:
        # Validate pizza toppings and calculate total price
        for pizza in order.pizzas:
            if len(pizza.toppings)>5:
                return JSONResponse(status_code=400, content="One of the order has more than 5 toppings.")
            
        total_price = len(order.pizzas) * 10

        db_order = Orders(total_price=total_price)
        db.add(db_order)
        db.commit()
        # Create pizzas and toppings for the order 
        for pizza in order.pizzas:
            db_pizza = Pizzas(
                order_id=db_order.order_id,
                base=pizza.base.value,
                cheese=pizza.cheese.value,
            )
            db.add(db_pizza)
            db.commit()
            db_toppings = [
                PizzaTopping(pizza_id=db_pizza.pizza_id, name=name.value)
                for name in pizza.toppings
            ]
            db.add_all(db_toppings)
            db.commit()

        # Retrieve the created order, create a background task to update its status
        current_order = db.query(Orders).filter_by(order_id=db_order.order_id).first()
        pizzas = current_order.pizzas
        asyncio.create_task(update_order_status(db, db_order.order_id))

        order_data = {
            "order_id": current_order.order_id,
            "total_price": current_order.total_price,
            "pizzas": [
                {
                    "pizza_id": pizza.pizza_id,
                    "base": pizza.base.value,
                    "cheese": pizza.cheese.value,
                    "toppings": [topping.name.value for topping in pizza.toppings],
                }
                for pizza in pizzas
            ],
        }

        return JSONResponse(content=order_data)

    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error creating order") from e


@router.get("/order/{order_id}/", response_model=IOrder)
async def read_order(order_id: str, db: Session = Depends(MySQLBase.get_session)):
    try:
        # Retrieve the order from the database
        db_order = db.query(Orders).filter_by(order_id=order_id).first()

        # Return a 404 response if order is not found
        if not db_order:
            return JSONResponse(status_code=404, content="Order not found")

        pizzas = db_order.pizzas

        order_data = {
            "order_id": db_order.order_id,
            "total_price": db_order.total_price,
            "pizzas": [
                {
                    "pizza_id": pizza.pizza_id,
                    "base": pizza.base.value,
                    "cheese": pizza.cheese.value,
                    "toppings": [topping.name.value for topping in pizza.toppings],
                }
                for pizza in pizzas
            ],
        }

        return JSONResponse(content=order_data)
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal error!")
