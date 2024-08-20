from sqlalchemy.orm import Session
from models import VulnerabilityDB

def create_vulnerability(db: Session, vulnerability_data: dict):
    db_vulnerability = VulnerabilityDB(**vulnerability_data)
    db.add(db_vulnerability)
    db.commit()
    db.refresh(db_vulnerability)
    return db_vulnerability

def get_vulnerabilities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(VulnerabilityDB).offset(skip).limit(limit).all()
