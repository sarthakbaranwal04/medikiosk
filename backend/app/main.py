"""
FastAPI application entrypoint.

Phase 1 (Foundation): app factory, config, DB connection wiring, CORS,
logging, and a health-check endpoint. Additional routers are registered
here as later phases add them (auth, patients, intake, speech, documents,
summaries, doctor).
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.routers import health

settings = get_settings()
configure_logging()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description=(
            "Backend for the Patient Case Taking Software (SIH 2026, PS ID 26047). "
            "Assists doctors by structuring patient intake and prior-document "
            "information for review — it does not diagnose or make treatment decisions."
        ),
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)

    # Registered in later phases:
    # app.include_router(auth.router, prefix="/auth", tags=["auth"])
    # app.include_router(patients.router, prefix="/patients", tags=["patients"])
    # app.include_router(intake.router, prefix="/intake", tags=["intake"])
    # app.include_router(speech.router, prefix="/speech", tags=["speech"])
    # app.include_router(documents.router, tags=["documents"])
    # app.include_router(summaries.router, tags=["summaries"])
    # app.include_router(doctor.router, prefix="/doctor", tags=["doctor"])

    return app


app = create_app()
