from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
import os
import requests
from fastapi.staticfiles import StaticFiles

app = FastAPI()

DATA_DRIVER_URL = "http://test-security-data_driver-1:5000"

#serve the static folder to the server
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="./templates")

#Get data from the api and store it in the db using data_writer
@app.post("/fetch-and-store")
async def fetch_and_store():
    response = requests.post(f"{DATA_DRIVER_URL}/fetch-and-store")
    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail="Data driver error")
    return {"success": "Retrieving data from api"}

#Get the data from the db using data_writer
@app.get("/", response_class=HTMLResponse)
async def read_data(request: Request, page: int = 1, per_page: int = 10):
    response = requests.get(f"{DATA_DRIVER_URL}", params={"page": page, "per_page": per_page})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Data driver error")
    vulnerabilities = response.json()
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "vulnerabilities": vulnerabilities['vulnerabilities'], 
        "page": vulnerabilities['page'], 
        "total_pages": vulnerabilities['total_pages'],
        "pagination_range": vulnerabilities['pagination_range'],
        "per_page": vulnerabilities['per_page'],
        "has_previous": vulnerabilities['page'] > 1,
        "has_next": vulnerabilities['page'] < vulnerabilities['total_pages']

        })

