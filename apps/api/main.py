# apps/api/main.py
from fastapi import FastAPI
from debate_service.routes.ping import router as ping_router

app = FastAPI()
app.include_router(ping_router)

