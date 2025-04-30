from fastapi import FastAPI
from app.routers import invite, users

app = FastAPI()

# Integriere die beiden Router (Einladungen und Benutzer)
app.include_router(invite.router)
app.include_router(users.router)