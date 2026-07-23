from typing import List

from apscheduler import job
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Job
from app.parser.Base import BaseParser
from app.parser.ProfesiaSk import ProfesiaParser
from app.schemas import JobResponse, JobCreate
from app.database import get_db


router = APIRouter(prefix="/jobs", tags=['jobs'])

def fetch_offers_by(db, location: str | None = None, source: str | None = None, keyword: str | None = None, telegram_id: str | None = None) -> List[Job]:
    jobs = db.query(Job)
    if location:
        jobs = jobs.filter(Job.location == location)
    if source:
        jobs = jobs.filter(Job.source == source)
    if keyword:
        jobs = jobs.filter(Job.keyword == keyword)
    if telegram_id:
        jobs = jobs.filter(Job.telegram_id == telegram_id)
    return jobs.all()

@router.get("/", response_model=List[JobResponse])
def get_offers_by(location: str | None = None, source: str | None = None, keyword: str | None = None, db: Session = Depends(get_db)):
    return fetch_offers_by(db, location=location, source=source, keyword=keyword)

def get_parser(source: str):
    match (source):
        case "profesia.sk":
            parser = ProfesiaParser()
        case _:
            raise HTTPException(status_code=400, detail="Source not supported")
    return parser

@router.post("/parse", response_model=str)
def parse_jobs(keyword: str, location: str, source: str, db: Session = Depends(get_db)):
    parser = get_parser(source)
    added = parser.parse(db, location, keyword)
    return "Parsing completed. Added: " + str(added)

def delete_by(db, location: str | None = None, source: str | None = None, keyword: str | None = None, telegram_id: str | None = None):
    deletion = db.query(Job)
    if location:
        deletion = deletion.filter(Job.location == location)
    if source:
        deletion = deletion.filter(Job.source == source)
    if keyword:
        deletion = deletion.filter(Job.keyword == keyword)
    if telegram_id:
        deletion = deletion.filter(Job.telegram_id == telegram_id)
    deletion.delete()
    db.commit()

@router.delete("/offers", response_model=str)
def delete_offers(location: str | None = None, source: str | None = None, keyword: str | None = None, db: Session = Depends(get_db)):
    delete_by(db, location=location, source=source, keyword=keyword)
    return "Successful deletion"