from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import uuid
from .database import Base

# User-Tabelle für registrierte Benutzer
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_admin = Column(Boolean, default=False)

# InviteToken-Tabelle für einmalige Registrierungslinks
class InviteToken(Base):
    __tablename__ = "invite_tokens"

    token = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    used_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
