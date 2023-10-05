from pydantic import BaseModel


class Submission(BaseModel):
    text: str
