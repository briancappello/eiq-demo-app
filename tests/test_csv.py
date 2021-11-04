import io
import os

from flask import url_for
from typing import *


DATA_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'data')


def get_file(filename) -> Tuple[io.BytesIO, str]:
    with open(os.path.join(DATA_DIR, filename), 'rb') as f:
        data = f.read()

    return io.BytesIO(data), filename


def test_valid_csv(client):
    r = client.post(
        url_for('views.index'),
        content_type='multipart/form-data',
        data=dict(file=get_file('valid.csv')),
        follow_redirects=True,
    )
    assert 'CSV is valid!' in r.html


def test_missing_row(client):
    r = client.post(
        url_for('views.index'),
        content_type='multipart/form-data',
        data=dict(file=get_file('missing-row.csv')),
        follow_redirects=True,
    )
    assert 'CSV file must have exactly 10 data rows' in r.html


def test_missing_col(client):
    r = client.post(
        url_for('views.index'),
        content_type='multipart/form-data',
        data=dict(file=get_file('missing-col.csv')),
        follow_redirects=True,
    )
    assert 'CSV file must have exactly 3 data columns' in r.html


def test_missing_cell(client):
    r = client.post(
        url_for('views.index'),
        content_type='multipart/form-data',
        data=dict(file=get_file('missing-cell.csv')),
        follow_redirects=True,
    )
    assert 'All cells in the CSV file must contain data.' in r.html
