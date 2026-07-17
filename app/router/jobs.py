from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Job
from app.parser.ProfesiaSk import ProfesiaParser
from app.schemas import JobResponse, JobCreate
from app.database import get_db


router = APIRouter(prefix="/jobs", tags=['jobs'])


@router.get("/", response_model=List[JobResponse])
def get_offers(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs

@router.get("/{keyword}", response_model=List[JobResponse])
def get_offers_by_keyword(keyword: str, db: Session = Depends(get_db)):
    jobs = db.query(Job).filter(Job.keyword == keyword).all()
    return jobs

@router.post("/parse", response_model=str)
def parse_jobs(keyword: str, location: str, source: str, db: Session = Depends(get_db)):
    match(source):
        case "profesia":
            parser = ProfesiaParser()
            parser.parse(location, keyword, db)
        case _:
            raise HTTPException(status_code=400, detail="Source not supported")
    return "Parsing completed"