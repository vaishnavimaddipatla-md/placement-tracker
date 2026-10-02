from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

import models
from auth import get_current_user, get_db

router = APIRouter(prefix="/analytics", tags=["Analytics"])

STATUSES = ["Wishlist", "Applied", "Online Test", "Interview", "Offer", "Rejected"]
SUBMITTED = ["Applied", "Online Test", "Interview", "Offer", "Rejected"]
PROGRESSED = ["Online Test", "Interview", "Offer"]


@router.get("")
def get_analytics(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    rows = (
        db.query(models.Application.status, func.count(models.Application.id))
        .filter(models.Application.user_id == user.id)
        .group_by(models.Application.status)
        .all()
    )
    current = dict(rows)
    by_status = [{"status": s, "count": current.get(s, 0)} for s in STATUSES]

    def ever_reached(statuses):
        return (
            db.query(func.count(func.distinct(models.StageHistory.application_id)))
            .select_from(models.StageHistory)
            .join(models.Application, models.Application.id == models.StageHistory.application_id)
            .filter(
                models.Application.user_id == user.id,
                models.StageHistory.to_status.in_(statuses),
            )
            .scalar()
            or 0
        )

    submitted = ever_reached(SUBMITTED)
    progressed = ever_reached(PROGRESSED)

    return {
        "total": sum(current.values()),
        "by_status": by_status,
        "interviews": ever_reached(["Interview"]),
        "offers": ever_reached(["Offer"]),
        "response_rate": round(progressed / submitted * 100) if submitted else 0,
    }