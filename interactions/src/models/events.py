from __future__ import annotations

import time
from pydantic import BaseModel, Field
from typing import Literal

class InteractEvent(BaseModel):
    user_id: str = Field(description="identifier of user")
    item_id: str = Field(description="identifier of interacted item")
    action: Literal['like', 'dislike'] = Field(description="positive or negative reaction for items")
    timestamp: float | None = Field(time.time(), description="timestamp of event")
