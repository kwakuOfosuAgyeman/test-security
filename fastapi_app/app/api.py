from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .nist_api import fetch_vulnerabilities

router = APIRouter()

@router.get("/vulnerabilities/")
async def get_vulnerabilities(page: int = 1, per_page: int = 10, db: Session = Depends(get_db)):
    try:
        vulnerabilities = fetch_vulnerabilities(page, per_page)
        return vulnerabilities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
