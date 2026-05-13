from pydantic import BaseModel


class CreateIdeaResponse(BaseModel):
    id: int
