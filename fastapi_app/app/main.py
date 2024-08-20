from fastapi import FastAPI, Request, Depends
from starlette.responses import HTMLResponse
from app.api import router as api_router
from app.database import get_db

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_data(request: Request, db: Session = Depends(get_db), page: int = 1, per_page: int = 10):
    response = requests.get(f"{DATA_DRIVER_URL}/vulnerabilities?page={page}&per_page={per_page}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Data driver error")
    vulnerabilities = response.json()
    return templates.TemplateResponse("table.html", {"request": request, "vulnerabilities": vulnerabilities})

app.include_router(api_router)
