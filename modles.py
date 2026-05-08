from sqlmodel import Field, SQLModel
from datetime import date


class Idea(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: date
