from app.parser.Base import *

class ProfesiaParser(BaseParser):
    def parse(self, db: Session, location: str, keyword: str, tg_id: str | None = None) -> int:
        res = 0
        location = location.lower()
        def parse_page(page):
            response = requests.get(f"https://www.profesia.sk/praca/{location}/?search_anywhere={keyword}&sort_by=relevance&page_num={page}")
            soup = BeautifulSoup(response.text, "html.parser")
            offers = soup.main.find_all("li")
            added = 0
            for offer in offers:
                try:
                    url = "profesia.sk" + offer.h2.a.get("href")
                    clean_url = url.split("?")[0]
                    db_job = Job(
                        title=offer.h2.span.text,
                        url=clean_url,
                        company=offer.find("span", "employer").text,
                        location=location,
                        keyword=keyword,
                        source="profesia.sk",
                        telegram_id=tg_id
                    )
                    existing = db.query(Job).filter(Job.url == db_job.url).first()
                    if not existing:
                        db.add(db_job)
                        added += 1
                except Exception:
                    pass
            return added
        i = 1
        while True:
            count = parse_page(i)
            res += count
            if count == 0:
                break
            i += 1
        db.commit()
        return res
