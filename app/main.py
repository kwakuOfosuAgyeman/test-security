from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
import requests

from schemas import Vulnerability
from .rabbitmq_utils import send_message, receive_message


app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_data(request: Request, page: int = 1, per_page: int = 10):
    # Send a request to the data driver to fetch vulnerabilities
    send_message("get_vulnerabilities", {"page": page, "per_page": per_page})

    # Wait for the data driver to process and store the data
    def callback(message):
        vulnerabilities = message.get("vulnerabilities", [])
        return templates.TemplateResponse("index.html", {"request": request, "vulnerabilities": vulnerabilities})

    # Here, you need a way to receive the response from the data driver; this is a placeholder
    response_message = receive_message("vulnerabilities_response", callback)
    return response_message

@app.post("/fetch_and_store_vulnerabilities/")
async def fetch_and_store_vulnerabilities():
    url = f"https://example.com/api/vulnerabilities?page={page}&per_page={per_page}"  # Replace with actual NIST API URL

    response = requests.get(url)
    if response.status_code == 200:
        vulnerabilities = response.json()
        # Send the fetched data to data_driver for storage
        send_message('fetch_vulnerabilities', {"vulnerabilities": vulnerabilities})
        return {"status": "Data fetching and storing initiated."}
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from API.")


@app.post("/save_vulnerability/")
async def save_vulnerability(vulnerability: Vulnerability):
    send_message("save_vulnerability", vulnerability.dict())
    return {"status": "Vulnerability data sent to data driver."}
