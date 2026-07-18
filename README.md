Job-Parser is a tool which main purpose is to look for job offers using keywords and location. 
To do it I am using bs4 to parse and requests to download html, Postgres and SQLAlchemy to keep offers in DB. 
You can use it through FastApi Swagger interface.
Also I implemented APScheduler. By default if project is active, it will trigger every day request "scheduled_profesia" at 9:00 am, you can change it if you'd like

## Stack
- Python
- Fast Api, beautifulsoup4, requests
- PostgreSQL, SQLAlchemy
- APScheduler
- Docker, docker-compose
  
## Guide
- Clone Repo
- type in terminal/bash docker-compose up --build
- go to http://localhost:8001/docs in browser
- Done.

### POST jobs/parse
Adds parsed job offers to DB. 3 query params: source, location, keyword

#Available sources:
- profesia.sk - type "profesia" in source field

### GET jobs/
Use to get saved offers. 3 query params to filter job offers, leave them empty to get all offers from DB

### DELETE jobs/offers
Use to delete offers. 3 query params, leave them empty to delete all offers from DB


## APScheduler
As I said, by default it runs scheduled_profesia function from scheduler.py. 
You can write your own function with chosen location, keyword and determine your time or interval (use scheduler.add_job(scheduled_profesia, 'interval', minutes=1))
Also my function scheduled_profesia write logs, you can keep it or omit it, code is simple
