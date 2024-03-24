from pydantic import BaseModel


class Token(BaseModel):  # type: ignore
    access_token: str
    token_type: str
