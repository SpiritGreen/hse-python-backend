from http import HTTPStatus
from typing import Annotated, List, Optional
from fastapi import APIRouter, HTTPException, Query, Response, status
from pydantic import NonNegativeInt, PositiveInt, NonNegativeFloat
from lecture_2.hw.shop_api.api.item.contracts import *
from lecture_2.hw.shop_api.api.store import queries as store

router = APIRouter(prefix='/item')

# POST add new item
@router.post('/', status_code=HTTPStatus.CREATED)
async def post_item(request: ItemRequest, response: Response) -> ItemResponse:
    item = store.add_item(request.as_item_info())
    response.headers['location'] = f'/item/{item.id}'
    return ItemResponse.from_entity(item)

# GET get item
@router.get('/{item_id}')
async def get_item(item_id: int) -> ItemResponse:
    entity = store.get_item(item_id)

    if entity is None or entity.info.deleted:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f'Requested resource /item/{item_id} was not found'
        )
    
    return ItemResponse.from_entity(entity)

# GET get item list
@router.get('/')
async def get_items(
    offset: NonNegativeInt = 0,
    limit: PositiveInt = 10,
    min_price: NonNegativeFloat | None = None,
    max_price: NonNegativeFloat | None = None,
    show_deleted: bool = False
) -> list[ItemResponse]:
    
    filter = lambda info: all(
        [
            min_price is None or info.price >= min_price,
            max_price is None or info.price <= max_price,
            show_deleted or not info.deleted,
        ]
    )

    response = [
        ItemResponse.from_entity(entity)
        for entity in store.get_items(offset, limit, filter)
    ]
    
    return response

# PUT replace item
@router.put('/{id}')
async def replace_item(id: int, data: ItemRequest) -> ItemResponse:
    info = data.as_item_info()
    changed_item = store.replace_item(id, info)
    if changed_item is None:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Request resource /item/{id} was not found'
        )
    return ItemResponse.from_entity(changed_item)

# PATCH update item
@router.patch('/{id}')
async def patch_item(id: int, item_data: ItemPatchRequest) -> ItemResponse:
    patch_info = item_data.as_item_patch_info()
    patched_item = store.patch_item(id, patch_info)

    if patched_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Request resource /item/{id} was not found'
        )
    if patched_item.info.deleted == True:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail=f'Request resource /item/{id} was not modified as it is deleted'
        )

    
    return ItemResponse.from_entity(patched_item)
        

# DELETE delete item
@router.delete(
    '/{id}',
    responses={
        HTTPStatus.OK: {
            'description': 'Successfully returned requested item'
        },
        HTTPStatus.NOT_FOUND: {
            'description': 'Failed to return requested item as one was not found'
        }
    },
    status_code=HTTPStatus.OK
)
async def delete_item(id: int) -> Response:
    entity = store.delete_item(id)
    if not entity:
        raise HTTPException(
                HTTPStatus.NOT_FOUND,
                f'Request resource /item/{id} was not found'
            )
    return Response("")
