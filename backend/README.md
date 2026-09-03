# Patient Case Taking Software — Backend

Backend for **Smart India Hackathon 2026, Problem Statement ID 26047**.

This system assists doctors during consultation by turning patient
self-check-in (voice/button intake + scanned prior prescriptions and
reports) into a concise, structured, **doctor-verified** case summary.
It is explicitly **not** a diagnostic system — every extracted field
must remain traceable to its source and is subject to doctor review
before it is treated as verified.

## Current status: Phase 1 — Foundation

This is being built in stages (see "Roadmap" below) rather than all at
once, so the codebase stays reviewable at each step. Phase 1 sets up:

- FastAPI app factory (`app/main.py`)
- Environment-driven configuration (`app/core/config.py`)
- PostgreSQL connection via SQLAlchemy (`app/core/database.py`)
- Alembic wired to the app's settings and shared metadata
- CORS configuration for the future React kiosk/doctor clients
- Basic structured logging
- A `/health` endpoint that also checks DB connectivity
- Project skeleton for the packages later phases will fill in
  (`models/`, `schemas/`, `routers/`, `services/`, `repositories/`)

No authentication, patient/case models, OCR, speech, or summary logic
exist yet — those arrive in Phases 2–7.

## Project structure

```
backend/
├── app/
│   ├── main.py                # FastAPI app factory + router registration
│   ├── core/
│   │   ├── config.py          # Settings (env-var driven)
│   │   ├── database.py        # Engine, session factory, declarative Base
│   │   ├── security.py        # Placeholder — filled in Phase 2
│   │   └── logging.py         # Logging setup
│   ├── models/                # SQLAlchemy models (Phase 2+)
│   ├── schemas/                # Pydantic schemas (Phase 2+)
│   ├── routers/
│   │   └── health.py          # GET /health
│   ├── services/               # Business logic (Phase 2+)
│   ├── repositories/           # DB access layer (Phase 2+)
│   └── utils/
├── tests/
│   └── test_health.py
├── alembic/
│   ├── env.py                  # Reads DATABASE_URL from app settings
│   ├── script.py.mako
│   └── versions/
├── .env.example
├── alembic.ini
├── requirements.txt
└── README.md
```

## Setup

### 1. Prerequisites

- Python 3.11+
- A running PostgreSQL instance

### 2. Install dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set at least `DATABASE_URL` to point at your Postgres
instance. Create the database first, e.g.:

```bash
createdb patient_case_db
```

### 4. Run database migrations

No models exist yet in Phase 1, so there's nothing to migrate — this
command will just work once Phase 2 adds the `User` model:

```bash
alembic revision --autogenerate -m "add user model"
alembic upgrade head
```

### 5. Start the API

```bash
uvicorn app.main:app --reload
```

- API base: http://localhost:8000
- Interactive docs (Swagger UI): http://localhost:8000/docs
- Health check: http://localhost:8000/health

### 6. Run tests

```bash
pytest
```

`tests/test_health.py` expects `DATABASE_URL` in `.env` to point at a
reachable Postgres instance (the health check reports `"database":
"unreachable"` rather than failing hard if it isn't, but you'll want a
real connection for later phases' tests).

## Design principles carried through every phase

- **Assistive, not autonomous**: the backend never produces a
  diagnosis or treatment decision — only a structured, editable
  summary for the doctor.
- **Traceability**: every extracted field keeps a reference to the
  original patient response or document it came from.
- **Doctor approval gate**: a case summary is not "verified" until a
  doctor has reviewed and approved it.
- **Confidence-aware**: low-confidence OCR/speech/extraction results
  are flagged for clarification or review rather than silently
  accepted.
- **Replaceable providers**: OCR (PaddleOCR) and speech (Bhashini/
  Whisper) sit behind service interfaces so the underlying provider
  can change without touching route handlers.
- **Data protection**: designed with the Digital Personal Data
  Protection Act, 2023 in mind — role-based access, no medical data in
  logs, secrets only via environment variables.

## Roadmap

| Phase | Scope |
|---|---|
| 1 ✅ | Foundation: FastAPI, config, DB, Alembic, health check |
| 2 | Authentication: User model, register/login, JWT, roles |
| 3 | Patient intake: Patient model, sessions, questions, responses, language selection |
| 4 | Document processing: upload, secure storage, PaddleOCR integration, confidence handling |
| 5 | Speech: Whisper/Bhashini service abstraction, transcription, low-confidence clarification |
| 6 | Case summary: structured extraction, summary generation, source references |
| 7 | Doctor dashboard APIs: case listing, summary retrieval, verification, approval |

Say the word when you're ready for Phase 2 and I'll add the `User`
model, registration/login endpoints, JWT issuance, and role-based
authorization on top of this foundation.
