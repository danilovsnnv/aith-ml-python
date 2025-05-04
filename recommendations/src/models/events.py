from __future__ import annotations

from pydantic import BaseModel, Field


class NewItemsEvent(BaseModel):
    item_ids: list[str] = Field(description="identifiers of new items")
