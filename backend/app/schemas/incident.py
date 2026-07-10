from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class IncidentCreate(BaseModel):
    title: str
    description: str
    severity: str
    risk_score: int
    mitre_technique_id: str


class IncidentUpdate(BaseModel):
    status: str


class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    severity: str
    status: str
    risk_score: int
    mitre_technique_id: str
    created_at: datetime