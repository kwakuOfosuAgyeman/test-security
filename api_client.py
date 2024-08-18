# app/api_client.py
import requests
import os
from typing import List
from models import Vulnerability

class APIClient:
    def __init__(self):
        self.api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName=cpe:2.3:o:microsoft:windows_10:1607"
        self.limit = 100
        self.offset = 0

    def fetch_data(self) -> List[Vulnerability]:
        response = requests.get(self.api_url)
        if response.status_code == 200:
            try:
                response_data = response.json()
                vulnerabilities = [Vulnerability(**item) for item in response_data["vulnerabilities"]]
                return vulnerabilities
            except requests.exceptions.JSONDecodeError:
                print("Error decoding JSON: Empty or invalid JSON response")
                response_data = None
        else:
            print(f"Error: Received response with status code {response.status_code}")
            response_data = None
            return response_data
        
