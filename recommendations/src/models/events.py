from __future__ import annotations

import time
from pydantic import BaseModel, Field
from typing import Literal

class InteractEvent(BaseModel):
    user_id: str = Field(description="identifier of user")
    item_ids: list[str] = Field(description="identifiers of interacted items")
    actions: list[Literal['like', 'dislike']] = Field(description="positive or negative reaction for items")
    timestamp: float | None = Field(time.time(), description="timestamp of event")


class NewItemsEvent(BaseModel):
    item_ids: list[str] = Field(description="identifiers of new items")
