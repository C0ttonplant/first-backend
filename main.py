from typing import List
from fastapi import FastAPI
from modles import Idea
from datetime import date

app = FastAPI()

ideas: List[Idea] = []


@app.get("/")
async def hello() -> str:
    return "hello from Riley Buck"


@app.get("/ideas")
async def get_ideas() -> List[Idea]:
    return ideas


@app.post("/ideas")
async def create_idea(title: str, content: str):
    idea = Idea(title=title, content=content, created_at=date.today())
    ideas.append(idea)
