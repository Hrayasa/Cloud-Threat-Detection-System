from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TimelineCreate(BaseModel):
    incident_id: int
    event_type: str
    details: str


class TimelineResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    incident_id: int
    event_type: str
    details: str
    timestamp: datetime