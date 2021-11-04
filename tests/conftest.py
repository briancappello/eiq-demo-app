import pytest

from flask import Response
from werkzeug.utils import cached_property

from app import create_app


class HtmlTestResponse(Response):
    """
    Like :class:`flask.wrappers.Response`, except extended with methods for inspecting
    the parsed URL and automatically decoding the response to a string.
    """

    @cached_property
    def html(self):
        """
        Returns the response's data parsed to a string of html.
        """
        return self.data.decode('utf-8')


@pytest.fixture(autouse=True, scope='session')
def app():
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture()
def client(app):
    app.response_class = HtmlTestResponse
    with app.test_client() as client:
        yield client
