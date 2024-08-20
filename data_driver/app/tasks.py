from .database import SessionLocal
from .models import VulnerabilityDB

def process_vulnerability(data):
    db = SessionLocal()
    try:
        vulnerability = VulnerabilityDB(**data)
        db.add(vulnerability)
        db.commit()
    except Exception as e:
        print(f"Failed to process vulnerability: {e}")
    finally:
        db.close()
