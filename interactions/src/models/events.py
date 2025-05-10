from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Literal

class InteractEvent(BaseModel):
    item_id: str = Field(description='identifier of interacted item')
    action: Literal['like', 'dislike'] = Field(description='positive or negative reaction for items')
