"""Fixtures for OAuth2 clients"""
import uuid
import json
import datetime

import pytest

from gn3.auth import db
from gn3.auth.authentication.oauth2.models.oauth2client import OAuth2Client

@pytest.fixture(autouse=True)
def fixture_patch_envvars(monkeypatch):
    monkeypatch.setenv("AUTHLIB_INSECURE_TRANSPORT", "true")

@pytest.fixture
def fixture_oauth2_clients(fixture_users_with_passwords):
    """Fixture: Create the OAuth2 clients for use with tests."""
    conn, users = fixture_users_with_passwords
    now = datetime.datetime.now()

    clients = tuple(
        OAuth2Client(str(uuid.uuid4()), f"yabadabadoo_{idx:03}", now,
         now + datetime.timedelta(hours = 2),
         {
             "client_name": f"test_client_{idx:03}",
             "scope": ["user", "profile"],
             "redirect_uri": "/test_oauth2",
             "token_endpoint_auth_method": [
                 "client_secret_post", "client_secret_basic"],
             "grant_types": ["password"]
         }, user)
        for idx, user  in enumerate(users, start=1))

    with db.cursor(conn) as cursor:
        cursor.executemany(
            "INSERT INTO oauth2_clients VALUES (?, ?, ?, ?, ?, ?)",
            ((str(client.client_id), client.client_secret,
              int(client.client_id_issued_at.timestamp()),
              int(client.client_secret_expires_at.timestamp()),
              json.dumps(client.client_metadata), str(client.user.user_id))
            for client in clients))

    yield conn, clients

    with db.cursor(conn) as cursor:
        cursor.executemany(
            "DELETE FROM oauth2_clients WHERE client_id=?",
            ((str(client.client_id),) for client in clients))
