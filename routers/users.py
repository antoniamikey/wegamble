from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database, auth
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

# Registrierung über Invite-Link
@router.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(database.SessionLocal)):
    token = db.query(models.InviteToken).filter(models.InviteToken.token == user.invite_token).first()
    if not token or token.used_by_user_id is not None:
        raise HTTPException(status_code=400, detail="Invalid or used invite token")
    if (datetime.utcnow() - token.created_at) > timedelta(hours=1):
        raise HTTPException(status_code=400, detail="Invite token expired")

    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = models.User(
        username=user.username,
        password_hash=auth.get_password_hash(user.password),
        is_admin=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token.used_by_user_id = new_user.id
    db.commit()
    return {"msg": "Registration successful"}

# Login mit JWT-Ausgabe
@router.post("/login", response_model=schemas.TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.SessionLocal)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
