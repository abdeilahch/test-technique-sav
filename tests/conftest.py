import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.db.init_db import init_db

@pytest.fixture(scope="session")
def client():
    init_db()
    app = create_app()
    return TestClient(app)
