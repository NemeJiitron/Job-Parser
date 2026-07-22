from pydantic import BaseModel


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    url: str
    keyword: str
    source: str
    telegram_id: str | None = None
    class Config:
        from_attributes = True

class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    url: str
    keyword: str
    source: str
    telegram_id: str | None = None
