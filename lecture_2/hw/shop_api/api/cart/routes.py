from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Response, status
from pydantic import NonNegativeInt, PositiveInt, NonNegativeFloat
from lecture_2.hw.shop_api.api.store import queries
from lecture_2.hw.shop_api.api.cart.contracts import *
from lecture_2.hw.shop_api.api.store.models import *

router = APIRouter(prefix='/cart')

# POST add new cart
@router.post('/', status_code=HTTPStatus.CREATED)
async def post_cart(response: Response) -> PostCartResponse:
    cart = queries.add_cart()
    response.headers['location'] = f'{router.prefix}/{cart.id}'
    return PostCartResponse.from_entity(cart)

# GET get cart
@router.get('/{id}')
async def get_cart(id: int) -> CartResponse:
    entity = queries.get_cart(id)

    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Request resource /cart/{id} was not found'
        )
    
    return CartResponse.from_entity(entity)

# GET get cart list
@router.get('/')
async def get_carts(
    offset: NonNegativeInt = 0,
    limit: PositiveInt = 10,
    min_price: NonNegativeFloat | None = None,
    max_price: NonNegativeFloat | None = None,
    min_quantity: NonNegativeInt | None = None,
    max_quantity: NonNegativeInt | None = None
) -> list[CartResponse]:
    
    def _filter(info: CartInfo):
        quantity = sum(item.quantity for item in info.items)
        return all(
            (
                min_price is None or info.price >= min_price,
                max_price is None or info.price <= max_price,
                min_quantity is None or quantity >= min_quantity,
                max_quantity is None or quantity <= max_quantity,
            )
        )
    
    carts = [
        CartResponse.from_entity(entity)
        for entity in queries.get_carts(offset, limit, _filter)
    ]

    return carts

# POST add item to cart
@router.post('/{cart_id}/add/{item_id}')
async def add_item_to_cart(cart_id: int, item_id: int) -> PostCartItemResponse:
    cart_item = queries.add_item_to_cart(cart_id, item_id)
    if cart_item is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f'Request resource /cart/{id} was not found'
        )
    return PostCartItemResponse.from_info(cart_item)
