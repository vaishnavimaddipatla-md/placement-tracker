from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

import models
import schemas
from auth import get_current_user, get_db

router = APIRouter(prefix="/applications", tags=["Applications"])


def get_own_application(app_id: int, db: Session, user: models.User) -> models.Application:
    application = (
        db.query(models.Application)
        .filter(models.Application.id == app_id, models.Application.user_id == user.id)
        .first()
    )
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.post("", response_model=schemas.ApplicationOut, status_code=201)
def create_application(
    data: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    application = models.Application(user_id=user.id, **data.model_dump())
    db.add(application)
    db.flush()
    db.add(
        models.StageHistory(
            application_id=application.id,
            from_status=None,
            to_status=application.status,
        )
    )
    db.commit()
    db.refresh(application)
    return application


@router.get("", response_model=List[schemas.ApplicationOut])
def list_applications(
    status: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    query = db.query(models.Application).filter(models.Application.user_id == user.id)
    if status:
        query = query.filter(models.Application.status == status)
    if search:
        like = f"%{search}%"
        query = query.filter(
            or_(models.Application.company.ilike(like), models.Application.role.ilike(like))
        )
    return (
        query.order_by(models.Application.updated_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{app_id}", response_model=schemas.ApplicationOut)
def get_application(
    app_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    return get_own_application(app_id, db, user)


@router.patch("/{app_id}", response_model=schemas.ApplicationOut)
def update_application(
    app_id: int,
    data: schemas.ApplicationUpdate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    application = get_own_application(app_id, db, user)
    changes = data.model_dump(exclude_unset=True, exclude_none=True)

    new_status = changes.get("status")
    if new_status and new_status != application.status:
        db.add(
            models.StageHistory(
                application_id=application.id,
                from_status=application.status,
                to_status=new_status,
            )
        )

    for field, value in changes.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)
    return application


@router.delete("/{app_id}", status_code=204)
def delete_application(
    app_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    application = get_own_application(app_id, db, user)
    db.query(models.StageHistory).filter(models.StageHistory.application_id == app_id).delete()
    db.query(models.Reminder).filter(models.Reminder.application_id == app_id).delete()
    db.delete(application)
    db.commit()