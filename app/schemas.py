# app/models.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# CVE details
class CVE(BaseModel):
    id: Optional[str] = None
    sourceIdentifier: Optional[str] = None
    published: Optional[str] = None
    lastModified: Optional[str] = None


# Description details
class Description(BaseModel):
    lang: Optional[str] = None
    value: Optional[str] = None


# Configuration Node details
class ConfigurationNode(BaseModel):
    operator: Optional[str] = None
    negate: Optional[bool] = None
    cpe_match: Optional[List[Dict[str, Any]]] = None


# Configuration details
class Configuration(BaseModel):
    nodes: Optional[List[ConfigurationNode]] = None


# CVSS Data details
class CVSSData(BaseModel):
    version: Optional[str] = None
    vectorString: Optional[str] = None
    accessVector: Optional[str] = None
    accessComplexity: Optional[str] = None
    authentication: Optional[str] = None
    confidentialityImpact: Optional[str] = None
    integrityImpact: Optional[str] = None
    availabilityImpact: Optional[str] = None
    baseScore: Optional[float] = None


# CVSS Metric V2 details
class CVSSMetricV2(BaseModel):
    source: Optional[str] = None
    type: Optional[str] = None
    acInsufInfo: Optional[bool] = None
    baseSeverity: Optional[str] = None
    cvssData: Optional[CVSSData] = None
    exploitabilityScore: Optional[float] = None
    impactScore: Optional[float] = None
    obtainAllPrivilege: Optional[bool] = None
    obtainOtherPrivilege: Optional[bool] = None
    obtainUserPrivilege: Optional[bool] = None
    userInteractionRequired: Optional[bool] = None


# Metric details
class Metric(BaseModel):
    cvssMetricV2: Optional[List[CVSSMetricV2]] = None


# Reference details
class Reference(BaseModel):
    source: Optional[str] = None
    url: Optional[str] = None
    tags: Optional[List[str]] = None


# Weakness details
class WeaknessDescription(BaseModel):
    lang: Optional[str] = None
    value: Optional[str] = None


class Weakness(BaseModel):
    source: Optional[str] = None
    type: Optional[str] = None
    description: Optional[List[WeaknessDescription]] = None


# Main CVEItem model
class CVEItem(BaseModel):
    cve: Optional[CVE] = None
    cisaActionDue: Optional[str] = None
    cisaExploitAdd: Optional[str] = None
    cisaRequiredAction: Optional[str] = None
    cisaVulnerabilityName: Optional[str] = None
    configurations: Optional[List[Configuration]] = None
    cveTags: Optional[List[str]] = None
    descriptions: Optional[List[Description]] = None
    metrics: Optional[Metric] = None
    references: Optional[List[Reference]] = None
    vulnStatus: Optional[str] = None
    weaknesses: Optional[List[Weakness]] = None

    class Config:
        extra = "allow"


class Vulnerability(BaseModel):
    cve: CVEItem
