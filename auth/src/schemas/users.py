from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    username: str = Field()
    balance: float = Field(default=0.0)

    model_config = {'from_attributes': True}
