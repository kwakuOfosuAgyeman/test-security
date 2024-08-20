FROM python:3.11-slim

WORKDIR /app

COPY ./app /app 

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
