from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vulnerability import Base, VulnerabilityDB
from models import Vulnerability
from rabbitmq_utils import send_message, receive_message
import requests
import json
import pika

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup():
    # Create database tables
    Base.metadata.create_all(bind=engine)

@app.post("/save_vulnerability/")
async def save_vulnerability(vulnerability: Vulnerability):
    db = SessionLocal()
    db_vulnerability = VulnerabilityDB(**vulnerability.dict())
    db.add(db_vulnerability)
    db.commit()
    db.refresh(db_vulnerability)
    db.close()
    return {"status": "Vulnerability saved successfully."}



@app.on_event("startup")
async def startup():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='fetch_vulnerabilities')
    channel.queue_declare(queue='vulnerabilities_response')

    def callback(ch, method, properties, body):
        message = json.loads(body)
        if method.routing_key == 'fetch_vulnerabilities':
            fetch_vulnerabilities(message)
        elif method.routing_key == 'vulnerabilities_response':
            send_message('frontend_response', message)

    channel.basic_consume(queue='fetch_vulnerabilities', on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue='vulnerabilities_response', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
