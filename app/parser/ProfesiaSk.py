from app.parser.Base import *

class ProfesiaParser(BaseParser):
    def parse(self, location: str, keyword: str, db: Session) -> list:
        response = requests.get(f"https://www.profesia.sk/praca/{location}/?search_anywhere={keyword}&sort_by=relevance")
        soup = BeautifulSoup(response.text, "html.parser")
        offers = soup.find_all("li")
        res = []
        for offer in offers:
            try:
                db_job = Job(
                    title=offer.h2.span.text,
                    url=offer.h2.a.get("href"),
                    company=offer.find("span", "employer").text,
                    location=location,
                    keyword=keyword,
                    source="profesia.sk"
                )
                res.append(db_job)
                db.add(db_job)
            except Exception:
                pass
        db.commit()
        return res
