from zoneinfo import ZoneInfo
from sqlmodel import Session, select
from app.models import URL
from datetime import datetime

def create_short_url(session: Session, url: str, short_code: str) -> URL:
    
    entry = URL(
        url=url,
        short_code=short_code,
        created_at=datetime.now(tz=ZoneInfo("Asia/Kolkata")),
        updated_at=datetime.now(tz=ZoneInfo("Asia/Kolkata"))
    )
    
    session.add(entry)
    session.commit()
    
    return entry


def get_short_url(session: Session, short_code: str) -> URL | None:
    return session.exec(
        select(URL).where(URL.short_code == short_code)
    ).first()
    

def increment_access_count(session: Session, short_code: str):    
    entry = get_short_url(session, short_code)
    if entry is not None:
        entry.access_count += 1
        session.add(entry)
        session.commit()
  
     
def update_short_url(session: Session, url: str, short_code: str) -> URL:
    entry = get_short_url(session, short_code)
    
    if entry:
        entry.url = url
        entry.updated_at = datetime.now(tz=ZoneInfo("Asia/Kolkata"))
        
        session.add(entry)
        session.commit()
        
    return entry
  

def delete_short_url(session: Session, short_code: str):
    entry = get_short_url(session, short_code)
    if entry is not None:
        session.delete(entry)
        session.commit()