from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
import os
import pika
import json
import requests
from fastapi.staticfiles import StaticFiles
from api_client import APIClient

app = FastAPI()
RABBITMQ_HOST = "rabbitmq"
api_client = APIClient()
DATA_DRIVER_URL = "http://test-security-repo-data_driver-1:5000"

# Mocked Data for In-Memory Cache
cache = {
    "vulnerabilities": [],
    "total": 0
}

#serve the static folder to the server
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="./templates")

def send_message(queue: str, message: dict):
    """Send a message to a RabbitMQ queue."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(message))
    connection.close()

def receive_message(queue: str) -> dict:
    """Receive a message from a RabbitMQ queue."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    method_frame, header_frame, body = channel.basic_get(queue)
    if method_frame:
        channel.basic_ack(method_frame.delivery_tag)
        connection.close()
        return json.loads(body)
    else:
        connection.close()
        raise HTTPException(status_code=500, detail="No message received from data driver.")

def update_cache(data):
    cache["vulnerabilities"] = data
    cache["total"] = len(data)


def fetch_data_from_cache(page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return cache["vulnerabilities"][start:end]

#Get data from the api and store it in the db using data_writer
@app.post("/fetch-and-store")
async def fetch_and_store():
    # Send a message to the data_driver to fetch and store data
    send_message("store_vulnerabilities", {"action": "fetch_and_store"})
    return {"success": "Data fetching and storing initiated."}

# Get the data from the db using data_writer
@app.get("/", response_class=HTMLResponse)
async def read_data(request: Request, page: int = 1, per_page: int = 10):
    if not cache["vulnerabilities"]:
        fetched_data = api_client.fetch_data()
        update_cache(fetched_data)

    # Calculate pagination
    vulnerabilities = fetch_data_from_cache(page, per_page)
  
    total = cache["total"]
    total_pages = (total + per_page - 1) // per_page
    pagination_range = get_pagination_range(page, total_pages)

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "vulnerabilities": vulnerabilities, 
        "page": page, 
        "total_pages": total_pages,
        "pagination_range": pagination_range,
        "per_page": per_page,
        "has_previous": page > 1,
        "has_next": page < total_pages
    })


def get_pagination_range(current_page: int, total_pages: int) -> list:
    """Generate a range of page numbers for pagination."""
    window = 2  # Number of pages to show before and after the current page
    pagination = []

    # Add first page
    if total_pages > 1:
        pagination.append(1)

    # Add pages around the current page
    start = max(2, current_page - window)
    end = min(total_pages - 1, current_page + window)
    if start < end:
        pagination.extend(range(start, end + 1))

    # Add last page
    if total_pages > 1 and end < total_pages:
        pagination.append(total_pages)

    return pagination
