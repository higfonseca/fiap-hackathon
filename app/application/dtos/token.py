from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):  # type: ignore
    access_token: str
    token_type: str


class TokenData(BaseModel):  # type: ignore
    user_id: UUID | None = None
