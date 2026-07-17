from sqlalchemy.orm import Session
import requests
from bs4 import BeautifulSoup
from app.models import Job

class BaseParser:
    def parse(self, location: str, keyword: str, db: Session) -> list:
        raise NotImplementedError()