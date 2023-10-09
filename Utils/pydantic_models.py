from enum import Enum
from typing import List
from pydantic import BaseModel


class IPizzaBase(Enum):
    THIN_CRUST = "thin_crust"
    NORMAL = "normal"
    CHEESE_BURST = "cheese_burst"


class ICheese(Enum):
    MOZZARELLA = "mozzarella"
    CHEDDAR = "cheddar"
    PARMESAN = "parmesan"
    BLUE = "blue"


class ITopping(Enum):
    PEPPERONI = "pepperoni"
    MUSHROOM = "mushroom"
    OLIVES = "olives"
    ONIONS = "onions"
    PEPPERS = "peppers"
    SAUSAGE = "sausage"
    BACON = "bacon"


class IOrderStatus(Enum):
    PLACED = "Placed"
    ACCEPTED = "Accepted"
    PREPARING = "Preparing"
    DISPATCHED = "Dispatched"
    DELIVERED = "Delivered"


class IPizza(BaseModel):
    base: IPizzaBase
    cheese: ICheese
    toppings: List[ITopping]


class IOrder(BaseModel):
    pizzas: List[IPizza]
