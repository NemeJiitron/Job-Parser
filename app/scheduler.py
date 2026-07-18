from apscheduler.schedulers.background import BackgroundScheduler
from app.parser.ProfesiaSk import ProfesiaParser
from app.database import Session_local
from datetime import datetime

def scheduled_profesia():
    db = Session_local()
    try:
        parser = ProfesiaParser()
        added = parser.parse('bratislava', 'studentska brigada', db)
        with open("logs.txt", "a") as f:
            f.write(f"{datetime.today()}: added {added} offers with keyword - studentska brigada\n")
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_profesia, 'cron', hour=9, minute=0)
