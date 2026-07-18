from typing import List

from apscheduler import job
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Job
from app.parser.ProfesiaSk import ProfesiaParser
from app.schemas import JobResponse, JobCreate
from app.database import get_db


router = APIRouter(prefix="/jobs", tags=['jobs'])

@router.get("/", response_model=List[JobResponse])
def get_offers_by(location: str | None = None, source: str | None = None, keyword: str | None = None, db: Session = Depends(get_db)):
    jobs = db.query(Job)
    if location:
        jobs = jobs.filter(Job.location == location)
    if source:
        jobs = jobs.filter(Job.source == source)
    if keyword:
        jobs = jobs.filter(Job.keyword == keyword)
    return jobs.all()

@router.post("/parse", response_model=str)
def parse_jobs(keyword: str, location: str, source: str, db: Session = Depends(get_db)):
    added = 0
    match(source):
        case "profesia":
            parser = ProfesiaParser()
            added = parser.parse(location, keyword, db)
        case _:
            raise HTTPException(status_code=400, detail="Source not supported")
    return "Parsing completed. Added: " + str(added)

@router.delete("/offers", response_model=str)
def delete_offers(location: str | None = None, source: str | None = None, keyword: str | None = None, db: Session = Depends(get_db)):
    deletion = db.query(Job)
    if location:
        deletion = deletion.filter(Job.location == location)
    if source:
        deletion = deletion.filter(Job.source == source)
    if keyword:
        deletion = deletion.filter(Job.keyword == keyword)
    deletion.delete()
    db.commit()
    return "Successful deletion"