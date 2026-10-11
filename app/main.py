from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.api import interviews, insights, jtbd

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Discovery Research Hub", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

app.include_router(interviews.router, prefix="/api/interviews", tags=["interviews"])
app.include_router(insights.router, prefix="/api/insights", tags=["insights"])
app.include_router(jtbd.router, prefix="/api/jtbd", tags=["jtbd"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "discovery-research-hub"}
