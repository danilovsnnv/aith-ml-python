from typing import Annotated

from pydantic import BaseModel, Field


class SignUpSchema(BaseModel):
    username: Annotated[str, Field(pattern=r"^[a-zA-Z0-9_]{5,32}$")]
    password: Annotated[str, Field(min_length=6, max_length=60)]


class SignInSchema(BaseModel):
    username: str
    password: str
