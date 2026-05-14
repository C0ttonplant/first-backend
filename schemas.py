from pydantic import BaseModel


class CreateIdeaResponse(BaseModel):
    id: int


class UpdateIdeaRequest(BaseModel):
    title: str | None = None
    content: str | None = None
