from __future__ import annotations

from pydantic import BaseModel, Field

class RecommendationResponse(BaseModel):
    img_id: int = Field(default='Poster id for frontend')
    title_id: str = Field(default='IMDB code for frontend')
    original_name: str = Field(description='Movie title')

    model_config = {'from_attributes': True}
