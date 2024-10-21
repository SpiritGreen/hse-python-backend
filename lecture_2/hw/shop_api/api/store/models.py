from dataclasses import dataclass
from pydantic import NonNegativeFloat, NonNegativeInt


# товар в корзине
@dataclass(slots=True)
class CartItemInfo:
    id: int                                                 # id товара
    name: str                                               # название
    quantity: NonNegativeInt                                # количество товара в корзине
    available: bool                                         # доступность (не удалён ли товар)

# корзина
@dataclass(slots=True)
class CartInfo:
    items: list[CartItemInfo]                               # список товаров в корзине
    price: NonNegativeFloat                                 # общая сумма заказа

@dataclass(slots=True)
class CartEntity:
    id: int                                                 # id корзины
    info: CartInfo

# товар
@dataclass(slots=True)
class ItemInfo:
    name: str | None = None                                 # название товара
    price: NonNegativeFloat | None = None                   # цена товара
    deleted: bool = False                                   # удалён ли товар

@dataclass(slots=True)
class ItemEntity:
    id: int                                                 # id товара
    info: ItemInfo

@dataclass(slots=True)
class ItemPatchInfo:
    name: str | None = None
    price: NonNegativeFloat | None = None