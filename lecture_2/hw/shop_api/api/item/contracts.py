from pydantic import BaseModel, ConfigDict, NonNegativeFloat
from lecture_2.hw.shop_api.api.store.models import *

class ItemRequest(BaseModel):
    name: str
    price: NonNegativeFloat
    deleted: bool = False
    
    def as_item_info(self) -> ItemInfo:
        return ItemInfo(
            name=self.name,
            price=self.price,
            deleted=self.deleted,
        )

class ItemResponse(BaseModel):
    id: int
    name: str
    price: NonNegativeFloat
    deleted: bool

    @staticmethod
    def from_entity(entity: ItemEntity) -> 'ItemResponse':
        return ItemResponse(
            id = entity.id,
            name = entity.info.name,
            price = entity.info.price,
            deleted = entity.info.deleted
        )

class ItemPatchRequest(BaseModel):
    name: str | None = None
    price: NonNegativeFloat | None = None
    model_config = ConfigDict(extra="forbid")

    def as_item_patch_info(self) -> ItemPatchInfo:
        return ItemPatchInfo(
            name = self.name,
            price = self.price,
        )
