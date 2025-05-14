from __future__ import annotations

from typing import Literal
from pydantic import BaseModel

from schemas.recommendations import RecommendationResponse


class MovieBase(BaseModel):
    img_id: int
    title_id: str
    poster_url: str
    item_type: Literal['Movie', 'TVSeries']
    name: str
    original_name: str
    description: str
    genre: list[str]
    date: str | None
    rating_count: float | None
    rating_value: float | None
    keywords: list[str]
    featured_review: str | None
    stars: list[str]
    directors: list[str]
    creators: list[str]

    model_config = {'from_attributes': True}

    def to_recommendation_response(self) -> RecommendationResponse:
        return RecommendationResponse(img_id=self.img_id, title_id=self.title_id, original_name=self.original_name)

class MovieIn(MovieBase):
    pass

class MovieOut(MovieBase):
    id: int
    class Config:
        orm_mode = True
