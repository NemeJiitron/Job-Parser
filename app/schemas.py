from pydantic import BaseModel


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    url: str
    keyword: str
    source: str

class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    url: str
    keyword: str
    source: str
