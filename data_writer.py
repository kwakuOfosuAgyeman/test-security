from sqlalchemy.orm import Session
from models import Vulnerability
from vulnerability import VulnerabilityDB
from api_client import APIClient

class DataWriter:
    def __init__(self):
        self.api_client = APIClient()

    #Fetch the data from the api
    def fetch_data(self):
        return self.api_client.fetch_data()

    #store the data of the api to the db
    def save_vulnerability(self, db: Session, vulnerability: Vulnerability):
        vulnerability_db = VulnerabilityDB(
            id=vulnerability.cve.id,
            sourceIdentifier=vulnerability.cve.sourceIdentifier,
            vulnStatus=vulnerability.cve.vulnStatus,
            published=vulnerability.cve.published,
            lastModified=vulnerability.cve.lastModified,
            cisaActionDue=str(vulnerability.cve.cisaActionDue),
            cisaExploitAdd=str(vulnerability.cve.cisaExploitAdd),
            cisaVulnerabilityName=vulnerability.cve.cisaVulnerabilityName,
            descriptions=str(vulnerability.cve.descriptions),
            weaknesses=str(vulnerability.cve.weaknesses),
            references=str(vulnerability.cve.references),
            configurations=str(vulnerability.cve.configurations),
            metrics=str(vulnerability.cve.metrics),
            cveTags=str(vulnerability.cve.cveTags)
        )
        # vulnerability_db.serialize_json_fields()
        db.add(vulnerability_db)
        db.commit()
        db.refresh(vulnerability_db)

        return vulnerability_db

    #call save_vulnerability
    def write_to_db(self, vulnerabilities, db: Session):
        for vulnerability in vulnerabilities:
            self.save_vulnerability(db, vulnerability)

    #get vulnerabilities data from the db
    def read_from_db(self, db: Session, page, per_page):
        total = db.query(VulnerabilityDB).count()
        total_pages = (total + per_page - 1) // per_page
        vulnerabilities = db.query(VulnerabilityDB).offset((page - 1) * per_page).limit(per_page).all()
        return {"vulnerabilities": vulnerabilities, "total_pages": total_pages}
