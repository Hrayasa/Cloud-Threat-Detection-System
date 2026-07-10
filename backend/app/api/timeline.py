from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.timeline import TimelineEvent
from app.schemas.timeline import TimelineResponse

router = APIRouter(
    prefix="/timeline",
    tags=["timeline"],
)


@router.get(
    "/",
    response_model=list[TimelineResponse],
    status_code=status.HTTP_200_OK,
)
def list_timeline_events(
    db: Session = Depends(get_db),
) -> list[TimelineResponse]:

    events = (
        db.query(TimelineEvent)
        .order_by(TimelineEvent.timestamp.desc())
        .all()
    )

    return [
        TimelineResponse.model_validate(event)
        for event in events
    ]


@router.get(
    "/{incident_id}",
    response_model=list[TimelineResponse],
    status_code=status.HTTP_200_OK,
)
def get_incident_timeline(
    incident_id: int,
    db: Session = Depends(get_db),
) -> list[TimelineResponse]:

    events = (
        db.query(TimelineEvent)
        .filter(TimelineEvent.incident_id == incident_id)
        .order_by(TimelineEvent.timestamp.desc())
        .all()
    )

    return [
        TimelineResponse.model_validate(event)
        for event in events
    ]