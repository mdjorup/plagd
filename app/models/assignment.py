from pydantic import BaseModel


class Assignment(BaseModel):
    id: int | None = None
    user_id: str | None = None
    title: str
    prompt: str
    word_limit: int
