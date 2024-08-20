from sqlalchemy import Column, String, DateTime, JSON,Enum, Text
from database import Base
import json

class VulnerabilityDB(Base):
    __tablename__ = "vulnerabilities"

    id = Column(String, primary_key=True, index=True)
    sourceIdentifier = Column(String, index=True)
    published = Column(String)
    lastModified = Column(String)
    vulnStatus = Column(String)
    cisaActionDue = Column(String)
    cisaExploitAdd = Column(String)
    cisaRequiredAction = Column(String)
    cisaVulnerabilityName = Column(String)
    cveTags = Column(Text)  # Store as JSON due to variable structure
    descriptions = Column(Text)  # Store as JSON due to variable structure
    metrics = Column(Text)  # Store as JSON due to variable structure
    configurations = Column(Text)  # Store as JSON due to variable structure
    references = Column(Text)  # Store as JSON due to variable structure
    weaknesses = Column(Text)  # Store as JSON due to variable structure


    def serialize_json_fields(self):
        """ Convert Python lists/dicts to JSON strings. """
        self.cveTags = json.dumps(self.cveTags)
        self.metrics = json.dumps(self.metrics)
        self.configurations = json.dumps(self.configurations)
        self.references = json.dumps(self.references)
        self.weaknesses = json.dumps(self.weaknesses)

    def deserialize_json_fields(self):
        """ Convert JSON strings back to Python lists/dicts. """
        self.cveTags = json.loads(self.cveTags)
        self.metrics = json.loads(self.metrics)
        self.configurations = json.loads(self.configurations)
        self.references = json.loads(self.references)
        self.weaknesses = json.loads(self.weaknesses)
