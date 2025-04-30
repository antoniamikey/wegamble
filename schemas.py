from pydantic import BaseModel
from typing import Optional

# Antwortmodell für JWT-Token
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Modell für Benutzerregistrierung
class UserCreate(BaseModel):
    username: str
    password: str
    invite_token: str

# Modell für Login-Daten
class UserLogin(BaseModel):
    username: str
    password: str

# Antwortmodell für Invite-Link-Erstellung
class InviteCreateResponse(BaseModel):
    token: str