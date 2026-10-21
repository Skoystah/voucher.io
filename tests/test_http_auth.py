"""Auth must be enforced on every mutating endpoint.

Before the hardening work the file-upload endpoint skipped the auth check
entirely (it was commented out), so these tests pin that down.
"""

import pytest
from fastapi.testclient import TestClient

from config import Config
from db.db import DB
from user.auth import get_jwt_token
from voucher.models import VoucherDB
from web.app import create_app

CSV_BODY = b"LEU121;1h\n"


@pytest.fixture
def client(config):
    return TestClient(create_app(config))


@pytest.fixture
def cookies(config):
    token = get_jwt_token("test", config.secret_key, 9999)
    return {"authToken": token}


def _upload(client, cookies=None):
    return client.post(
        "/vouchers/upload-file",
        files={"file": ("test.csv", CSV_BODY, "text/csv")},
        cookies=cookies or {},
    )


def test_upload_file_rejects_missing_token(client, config):
    res = _upload(client)

    assert res.status_code == 403


def test_upload_file_rejects_garbage_token(client, config):
    res = _upload(client, cookies={"authToken": "not-a-valid-token"})

    assert res.status_code == 403


def test_upload_file_rejects_token_signed_with_other_key(config, tmp_path):
    other_config = Config(
        DB(str(tmp_path / "other.db"), verbose=False), secret_key="a" * 32
    )
    client = TestClient(create_app(other_config))
    foreign_token = get_jwt_token("test", "b" * 32, 9999)

    res = _upload(client, cookies={"authToken": foreign_token})

    assert res.status_code == 403


def test_upload_file_accepts_valid_token(client, config, cookies):
    res = _upload(client, cookies=cookies)

    assert res.status_code == 201
    assert res.json()["created_count"] == 1


def test_upload_file_creates_nothing_without_auth(client, config):
    _upload(client)

    assert VoucherDB(config).get_vouchers() == []


@pytest.mark.parametrize(
    "method,path",
    [
        ("post", "/vouchers"),
        ("put", "/vouchers/LEU123"),
        ("delete", "/vouchers/LEU123"),
    ],
)
def test_mutating_endpoints_require_auth(client, method, path):
    # DELETE takes no request body, so only send JSON where one applies.
    kwargs = (
        {} if method == "delete" else {"json": {"code": "LEU123", "duration": "1h"}}
    )

    res = getattr(client, method)(path, **kwargs)

    assert res.status_code == 403


def test_mutating_endpoints_allowed_with_auth(client, config, cookies):
    db = VoucherDB(config)
    db.add_voucher("LEU123", "1h")

    assert client.put("/vouchers/LEU123", cookies=cookies).status_code == 200
    assert config.db.get_voucher("LEU123").used is True
