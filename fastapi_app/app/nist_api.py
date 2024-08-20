from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

# Define the URL for the NIST API and the Data Driver
NIST_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName=cpe:2.3:o:microsoft:windows_10:1607"
DATA_DRIVER_URL = "http://data_driver:8000"

@router.get("/vulnerabilities")
async def get_vulnerabilities(page: int = 1, per_page: int = 10):
    """
    This endpoint acts as a gateway to fetch vulnerabilities from the NIST API
    or from the data driver depending on the request parameters.
    """
    try:
        response = requests.get(f"{DATA_DRIVER_URL}/vulnerabilities", params={"page": page, "per_page": per_page})
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        raise HTTPException(status_code=500, detail=f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        raise HTTPException(status_code=500, detail=f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        raise HTTPException(status_code=500, detail=f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        raise HTTPException(status_code=500, detail=f"Request Error: {err}")
    
    return response.json()


