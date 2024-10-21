from pydantic import BaseModel, NonNegativeFloat
from lecture_2.hw.shop_api.api.store.models import *

class CartResponse(BaseModel):
    id: int
    items: list[CartItemInfo]
    price: NonNegativeFloat

    def from_entity(entity: CartEntity) -> 'CartResponse':
        return CartResponse(
            id=entity.id,
            items=entity.info.items,
            price=entity.info.price
        )

class PostCartResponse(BaseModel):
    id: int

    @staticmethod
    def from_entity(entity: CartEntity) -> "PostCartResponse":
        return PostCartResponse(id=entity.id) 

class PostCartItemResponse(BaseModel):
    id: int
    name: str
    quantity: int
    available: bool

    @staticmethod
    def from_info(info: CartItemInfo) -> "PostCartItemResponse":
        return PostCartItemResponse(
            id=info.id,
            name=info.name,
            quantity=info.quantity,
            available=info.available
        )