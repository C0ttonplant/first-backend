from typing import Sequence
from fastapi import FastAPI, Depends
from database import get_db
from schemas import CreateIdeaResponse
from modles import Idea
from sqlmodel import Session, select
from datetime import date

app = FastAPI()


@app.get("/")
async def hello() -> str:
    return "<!doctype html><html>hey!</html>"


@app.get("/ideas")
async def get_ideas(db: Session = Depends(get_db)) -> Sequence[Idea]:
    return db.exec(select(Idea)).all()


@app.post("/ideas")
async def create_idea(title: str, content: str, db: Session = Depends(get_db)) -> CreateIdeaResponse:
    idea = Idea(title=title, content=content, created_at=date.today())
    db.add(idea)
    db.commit()
    return CreateIdeaResponse(id=idea.id)
