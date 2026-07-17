from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.database import Base, engine, get_db
import app.models
from app.router import jobs


@asynccontextmanager
async def lifespan(application: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
app = FastAPI(lifespan=lifespan)
app.include_router(jobs.router)
@app.get("/")
def root():
    return {"project": "Job-Parser"}
