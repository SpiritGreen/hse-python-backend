from typing import Optional, Iterable, Callable, Iterator
from lecture_2.hw.shop_api.api.store.models import *
from lecture_2.hw.shop_api.api.item.contracts import *
from pydantic import PositiveInt

# генератор id для корзин
def int_cart_id_generator() -> Iterable[int]:
    i = 0
    while True:
        yield i
        i += 1

# генератор id для товаров
def int_item_id_generator() -> Iterable[int]:
    i = 0
    while True:
        yield i
        i += 1

_cart_data = dict[int, CartInfo]()
_id_cart_generator = int_cart_id_generator()

_item_data = dict[int, ItemInfo]()
_id_item_generator = int_item_id_generator()

# добавление новой корзины
def add_cart(info: CartInfo = None) -> CartEntity:
    if not info:
        info = CartInfo([], 0)
    _id = next(_id_cart_generator)
    _cart_data[_id] = info
    return CartEntity(_id, _cart_data[_id])

# получение корзины по id
def get_cart(cart_id: int) -> Optional[CartEntity]:
    if cart_id not in _cart_data:
        return None
    return CartEntity(cart_id, _cart_data[cart_id])

# получение списка корзин с query-параметрами
def get_carts(
        offset: NonNegativeInt,
        limit: PositiveInt,
        _filter: Callable[[CartInfo], bool] | None = None
) -> Iterator[CartEntity]:
    if _filter is None:
        _filter = lambda x: True

    entities = filter(
        lambda x: _filter(x.info), (CartEntity(id, info) for id, info in _cart_data.items())
    )

    curr = 0
    for entity in entities:
        if offset <= curr < offset + limit:
            yield entity        
        curr += 1    

# добавление предмета в корзину
def add_item_to_cart(cart_id: int, item_id: int) -> Optional[CartItemInfo]:
    if cart_id not in _cart_data:
        return None

    cart_info = _cart_data.get(cart_id)

    for cart_item_info in cart_info.items:
        if cart_item_info.id == item_id:
            cart_item_info.quantity += 1
            return cart_item_info

    item_info = _item_data[item_id]
    cart_item_info = CartItemInfo(item_id, item_info.name, 1, not item_info.deleted)
    cart_info.items.append(cart_item_info)

    return cart_item_info

# добавление нового предмета
def add_item(info: ItemInfo) -> ItemEntity:
    _id = next(_id_item_generator)
    _item_data[_id] = info
    return ItemEntity(_id, info)

# получение товара по id
def get_item(item_id: int) -> Optional[ItemEntity]:
    if item_id not in _item_data:
        return None
    return ItemEntity(item_id, _item_data.get(item_id))

# получение списка товаров с query-параметрами
def get_items(
        offset: NonNegativeInt,
        limit: PositiveInt,
        _filter: Callable[[ItemInfo], bool] | None = None,
) -> Iterator[ItemEntity]:

    if _filter is None:
        _filter = lambda x: True

    entities = filter(
        lambda x: _filter(x.info), (ItemEntity(id, info) for id, info in _item_data.items())
    )
   
    curr = 0
    for entity in entities:
        if offset <= curr < offset + limit:
            yield entity        
        curr += 1     

# замена товара по id
def replace_item(item_id: int, info: ItemInfo) -> Optional[ItemEntity]:
    if item_id not in _item_data:
        return None
    _item_data[item_id] = info
    return ItemEntity(item_id, info)

# частичное обновление товара по id
def patch_item(item_id: int, info: ItemPatchInfo) -> Optional[ItemEntity]:
    if item_id not in _item_data:
        return None
    
    item = _item_data.get(item_id)

    if not item.deleted:
        if info.name is not None:
            item.name = info.name
        if info.price is not None:
            item.price = info.price
    
    return ItemEntity(item_id, item)

# удаление товара по id
def delete_item(item_id: int) -> bool:
    if item_id not in _item_data:
        return False
    _item_data[item_id] = True
    for cart in _cart_data.values():
        for item in cart.items:
            if item.id == id:
                item.available = False
    return True