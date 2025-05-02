from __future__ import annotations

from pydantic import BaseModel, Field


class RecommendationsResponse(BaseModel):
    item_ids: list[str] = Field([], description="list of recommended items")