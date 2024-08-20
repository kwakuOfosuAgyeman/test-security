import requests
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi_app.app import nist_api
from app.database import get_db  # Assuming you have a database session dependency
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# Include the gateway router
app.include_router(nist_api.router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request, db: Session = Depends(get_db), page: int = 1, per_page: int = 10):
    vulnerabilities = fetch_vulnerabilities(db, page, per_page)
    return templates.TemplateResponse("index.html", {"request": request, "vulnerabilities": vulnerabilities})