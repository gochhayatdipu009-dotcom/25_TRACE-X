from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.scan import router as scan_router
from app.api.timeline import router as timeline_router

app = FastAPI(title="OSINT SaaS Backend")

# CORS (Vite frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 API ROUTERS (THIS WAS THE ISSUE)
app.include_router(scan_router, prefix="/api", tags=["Scan"])
app.include_router(timeline_router, prefix="/api", tags=["Timeline"])


@app.get("/health")
def health():
    return {"status": "ok"}
