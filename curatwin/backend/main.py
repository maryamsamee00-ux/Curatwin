import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .config import CORS_ORIGINS

from .routers import auth, users, wellness, stress, digital_twin, mood, cycle, coping, insights, guardians, consent, alerts

app = FastAPI(title="CuraTwin API", version="1.0.0", description="AI-Powered Digital Twin for University Female Well-Being")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(wellness.router)
app.include_router(stress.router)
app.include_router(digital_twin.router)
app.include_router(mood.router)
app.include_router(cycle.router)
app.include_router(coping.router)
app.include_router(insights.router)
app.include_router(guardians.router)
app.include_router(consent.router)
app.include_router(alerts.router)

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "CuraTwin API", "version": "1.0.0"}


for mount_path, sub_dir in [("/css", "css"), ("/js", "js"), ("/assets", "assets")]:
    mount_dir = os.path.join(FRONTEND_DIR, sub_dir)
    if os.path.isdir(mount_dir):
        app.mount(mount_path, StaticFiles(directory=mount_dir), name=sub_dir)


@app.get("/")
def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.get("/{path:path}")
def serve_spa(path: str):
    file_path = os.path.join(FRONTEND_DIR, path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
