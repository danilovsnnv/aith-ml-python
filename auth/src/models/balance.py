from pydantic.v1 import BaseModel, Field

class Balance(BaseModel):
    balance: float = Field(default=0.0)

class ChangeBalance(BaseModel):
    balance_change: float = Field(default=0.0)
