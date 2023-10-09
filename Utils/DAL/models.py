import datetime
import uuid

from sqlalchemy import Column, DateTime, Integer, CHAR, func, ForeignKey
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import relationship

from Utils.DAL.connector import MySQLBase
from enum import Enum as PyEnum


class PizzaBase(PyEnum):
    THIN_CRUST = "thin_crust"
    NORMAL = "normal"
    CHEESE_BURST = "cheese_burst"


class Cheese(PyEnum):
    MOZZARELLA = "mozzarella"
    CHEDDAR = "cheddar"
    PARMESAN = "parmesan"
    BLUE = "blue"


class Topping(PyEnum):
    PEPPERONI = "pepperoni"
    MUSHROOM = "mushroom"
    OLIVES = "olives"
    ONIONS = "onions"
    PEPPERS = "peppers"
    SAUSAGE = "sausage"
    BACON = "bacon"


class OrderStatus(PyEnum):
    PLACED = "Placed"
    ACCEPTED = "Accepted"
    PREPARING = "Preparing"
    DISPATCHED = "Dispatched"
    DELIVERED = "Delivered"


class BaseModel(MySQLBase):
    __abstract__ = True

    createdAt = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updatedAt = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class Orders(BaseModel):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(
        CHAR(36), default=uuid.uuid4, index=True, nullable=False, primary_key=True
    )
    order_time = Column(DateTime, default=datetime.datetime.utcnow)
    total_price = Column(Integer, nullable=False)

    status = Column(ENUM(OrderStatus), default=OrderStatus.PLACED, nullable=False)
    pizzas = relationship(
        "Pizzas", back_populates="order", cascade="all, delete-orphan"
    )


class Pizzas(BaseModel):
    __tablename__ = "pizzas"

    id = Column(Integer, primary_key=True, autoincrement=True)

    order_id = Column(
        CHAR(36), ForeignKey("orders.order_id", ondelete="CASCADE"), index=True
    )
    pizza_id = Column(
        CHAR(36), default=uuid.uuid4, index=True, nullable=False, primary_key=True
    )

    base = Column(ENUM(PizzaBase))
    cheese = Column(ENUM(Cheese))

    order = relationship("Orders", back_populates="pizzas")

    toppings = relationship(
        "PizzaTopping", back_populates="pizza", cascade="all, delete-orphan"
    )


class PizzaTopping(BaseModel):
    __tablename__ = "pizza_topping"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(ENUM(Topping))
    pizza_id = Column(CHAR(36), ForeignKey("pizzas.pizza_id", ondelete="CASCADE"))
    pizza = relationship("Pizzas", back_populates="toppings")
