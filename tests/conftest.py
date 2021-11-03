import pytest

from app import create_app


@pytest.fixture(autouse=True, scope='session')
def app():
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()
