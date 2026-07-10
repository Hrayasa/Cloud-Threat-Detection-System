from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.incident import Incident
from app.schemas.incident import (
    IncidentCreate,
    IncidentResponse,
    IncidentUpdate,
)

router = APIRouter(
    prefix="/incidents",
    tags=["incidents"],
)


@router.get(
    "/",
    response_model=list[IncidentResponse],
    status_code=status.HTTP_200_OK,
)
def list_incidents(
    db: Session = Depends(get_db),
) -> list[IncidentResponse]:

    incidents = (
        db.query(Incident)
        .order_by(Incident.created_at.desc())
        .all()
    )

    return [
        IncidentResponse.model_validate(incident)
        for incident in incidents
    ]


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse,
    status_code=status.HTTP_200_OK,
)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
) -> IncidentResponse:

    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )

    return IncidentResponse.model_validate(incident)


@router.post(
    "/",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_incident(
    payload: IncidentCreate,
    db: Session = Depends(get_db),
) -> IncidentResponse:

    incident = Incident(
        title=payload.title,
        description=payload.description,
        severity=payload.severity,
        risk_score=payload.risk_score,
        mitre_technique_id=payload.mitre_technique_id,
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return IncidentResponse.model_validate(incident)


@router.patch(
    "/{incident_id}",
    response_model=IncidentResponse,
    status_code=status.HTTP_200_OK,
)
def update_incident(
    incident_id: int,
    payload: IncidentUpdate,
    db: Session = Depends(get_db),
) -> IncidentResponse:

    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )

    incident.status = payload.status

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return IncidentResponse.model_validate(incident)