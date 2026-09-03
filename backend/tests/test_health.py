"""
Phase 1 smoke test: the app starts and the health endpoint responds.

Note: this hits a real DB session via the `db` dependency, so it expects
DATABASE_URL (see .env.example) to point at a reachable Postgres instance.
Later phases can override `get_db` with a test-database fixture.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check_returns_ok_status():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "database" in body
