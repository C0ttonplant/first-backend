from datetime import date
from typing import Sequence
from fastapi import FastAPI, Depends, status, HTTPException
from database import get_db
from schemas import CreateIdeaResponse, UpdateIdeaRequest
from modles import Idea
from sqlmodel import Session, select

app = FastAPI()


@app.get("/ideas")
async def get_ideas(db: Session = Depends(get_db)) -> Sequence[Idea]:
    return db.exec(select(Idea)).all()


@app.get("/ideas/{idea_id}")
async def get_idea(idea_id: int, db: Session = Depends(get_db)) -> Idea:
    idea: Idea | None = db.get(Idea, idea_id)

    if not idea:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Idea with id {idea_id}, Not Found")

    return idea


@app.post("/ideas", status_code=status.HTTP_201_CREATED)
async def create_idea(title: str, content: str, db: Session = Depends(get_db)) -> CreateIdeaResponse:
    idea = Idea(title=title, content=content, created_at=date.today())
    db.add(idea)
    db.commit()
    if not idea.id:
        raise HTTPException(status.HTTP_507_INSUFFICIENT_STORAGE)
    return CreateIdeaResponse(id=idea.id)


@app.patch("/ideas/{idea_id}", status_code=status.HTTP_204_NO_CONTENT)
async def patch_idea(idea_id: int, update: UpdateIdeaRequest, db: Session = Depends(get_db)) -> None:
    idea: Idea | None = db.get(Idea, idea_id)
    if not idea:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Idea with id {idea_id}, Not Found")

    if update.title:
        idea.title = update.title
    if update.content:
        idea.content = update.content
    db.commit()


@app.delete("/ideas/{idea_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_idea(idea_id: int, db: Session = Depends(get_db)) -> None:
    idea: Idea | None = db.get(Idea, idea_id)
    if not idea:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Idea with id {idea_id}, Not Found")
    db.delete(idea)
    db.commit()
