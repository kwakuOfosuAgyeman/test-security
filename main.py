from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db, engine
from data_writer import DataWriter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import vulnerability


vulnerability.Base.metadata.create_all(bind=engine)
app = FastAPI()

data_writer = DataWriter()


#Get data from the api and store it in the db using data_writer
@app.post("/fetch-and-store")
async def fetch_and_store(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    vulnerabilities = data_writer.fetch_data()
    if(vulnerabilities != None):
        background_tasks.add_task(data_writer.write_to_db, vulnerabilities, db)
        return JSONResponse(status_code=201, content={"status": "Data fetching and storing initiated."})
    else:
        return JSONResponse(status_code=400, content={"status": "Unable to retrieve data from API. Please try again later"})

#Get the data from the db using data_writer
@app.get("/")
async def read_data(db: Session = Depends(get_db), page: int = 1, per_page: int = 10):
    vulnerabilities = data_writer.read_from_db(db, page=page, per_page=per_page)
    pagination_range = get_pagination_range(page, vulnerabilities['total_pages'])
    return  {
        "vulnerabilities": vulnerabilities['vulnerabilities'], 
        "page": page, 
        "total_pages": vulnerabilities['total_pages'],
        "pagination_range": pagination_range,
        "per_page": per_page,
        "has_previous": page > 1,
        "has_next": page < vulnerabilities['total_pages']
    }


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