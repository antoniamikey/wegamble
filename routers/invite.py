from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .. import models, schemas, database, auth

router = APIRouter(prefix="/invite", tags=["invite"])

# Nur Admins können Invite-Links generieren
@router.post("/generate", response_model=schemas.InviteCreateResponse)
def generate_invite(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.SessionLocal)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    invite = models.InviteToken()
    db.add(invite)
    db.commit()
    return {"token": invite.token}