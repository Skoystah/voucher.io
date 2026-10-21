import json

import pytest
from fastapi.testclient import TestClient

from user.auth import get_jwt_token
from voucher.models import VoucherDB
from web.app import create_app


@pytest.fixture
def client(config):
    return TestClient(create_app(config))


@pytest.fixture
def cookies(config):
    token = get_jwt_token("test", config.secret_key, 9999)
    return {"authToken": token}


def test_handle_add_voucher(client, cookies):
    vouch = {"code": "LEU123", "duration": "1h"}

    expected_vouch = """
    {
        "code": "LEU123",
        "duration": "1h",
        "used": false
    }
    """

    res = client.post("/vouchers", json=vouch, cookies=cookies)

    assert res.json() == json.loads(expected_vouch)


def test_handle_add_vouchers_file_csv(client, cookies):
    expected_vouchers = """
    [
        {
                "code": "LEU5RJ6BXSS",
                "duration": "4h",
                "used": false
                },
        {
                "code": "LEU5RJ6BT34",
                "duration": "4h",
                "used": false
                },
        {
                "code": "LEU5RJ6BHPP",
                "duration": "4h",
                "used": false
                },
        {
                "code": "LEU5RJ6BCCG",
                "duration": "4h",
                "used": false
                },
        {
                "code": "LEU5RJ6BWWF",
                "duration": "4h",
                "used": false
                },
        {
                "code": "LEU5RJ6BHB9",
                "duration": "4h",
                "used": false
                },
        {
                "code": "LEU6J9BWEY8",
                "duration": "2h",
                "used": false
                }
        ]
    """

    with open("tests/data/test_vouchers.csv", "rb") as file:
        res = client.post(
            "/vouchers/upload-file",
            files={"file": ("test_vouchers.csv", file, "text/csv")},
            cookies=cookies,
        )
    assert res.json()["created_vouchers"] == json.loads(expected_vouchers)


def test_handle_add_vouchers_file_pdf(client, cookies):
    expected_vouchers = """
    [
        {
            "code": "LEU2CRPG36K",
            "duration": "2h",
            "used": false
            },
        {
            "code": "LEU2CRPGPS3",
            "duration": "2h",
            "used": false
            },
        {
            "code": "LEU2CRPGWAH",
            "duration": "2h",
            "used": false
            },
        {
            "code": "LEU2CRPGGE9",
            "duration": "2h",
            "used": false
            },
        {
            "code": "LEU2CRPGXKW",
            "duration": "2h",
            "used": false
            },
        {
            "code": "LEU2CRPGLFU",
            "duration": "2h",
            "used": false
            },
        {
            "code": "LEU2CRPG2F2",
            "duration": "2h",
            "used": false
            },
        {
            "code": "LEU2CRPGHSL",
            "duration": "2h",
            "used": false
            },
        {
            "code": "LEU2CRPGUR5",
            "duration": "2h",
            "used": false
            },
        {
            "code": "LEU2CRPGVD3",
            "duration": "2h",
            "used": false
            }
    ]
    """
    with open("tests/data/test_vouchers.pdf", "rb") as file:
        res = client.post(
            "/vouchers/upload-file",
            files={"file": ("test_vouchers.pdf", file, "application/pdf")},
            cookies=cookies,
        )
    assert res.json()["created_vouchers"] == json.loads(expected_vouchers)


def test_handle_list_voucher(client, cookies, config):
    voucher_codes = [
        "LEU123",
        "LEU456",
    ]
    voucher_durations = [
        "1h",
        "2h",
    ]

    voucherDB = VoucherDB(config)

    for code, duration in zip(voucher_codes, voucher_durations):
        voucherDB.add_voucher(code, duration)

    expected_vouchers = """
    [
        {
        "code": "LEU123",
        "duration": "1h",
        "used": false
        },
        {
        "code": "LEU456",
        "duration": "2h",
        "used": false
        }
    ]
    """

    res = client.get("/vouchers", cookies=cookies)

    assert res.json() == json.loads(expected_vouchers)


def test_handle_list_filtered_voucher_duration(client, cookies, config):
    voucher_codes = [
        "LEU123",
        "LEU456",
    ]
    voucher_durations = [
        "1h",
        "2h",
    ]

    voucherDB = VoucherDB(config)

    for code, duration in zip(voucher_codes, voucher_durations):
        voucherDB.add_voucher(code, duration)

    expected_vouchers = """
    [
        {
        "code": "LEU456",
        "duration": "2h",
        "used": false
        }
    ]
    """

    res = client.get("/vouchers?duration=2h", cookies=cookies)

    assert res.json() == json.loads(expected_vouchers)


def test_handle_list_filtered_voucher_used(client, cookies, config):
    voucher_codes = [
        "LEU123",
        "LEU456",
    ]
    voucher_durations = [
        "1h",
        "2h",
    ]

    voucherDB = VoucherDB(config)

    for code, duration in zip(voucher_codes, voucher_durations):
        voucherDB.add_voucher(code, duration)

    expected_vouchers = """
    [
        {
        "code": "LEU456",
        "duration": "2h",
        "used": false
        }
    ]
    """

    voucherDB.use_voucher("LEU123")

    res = client.get("/vouchers?includeUsed=false", cookies=cookies)

    assert res.json() == json.loads(expected_vouchers)


def test_handle_use_voucher(client, cookies, config):
    voucher_codes = [
        "LEU123",
        "LEU456",
    ]
    voucher_durations = [
        "1h",
        "2h",
    ]

    voucherDB = VoucherDB(config)

    for code, duration in zip(voucher_codes, voucher_durations):
        voucherDB.add_voucher(code, duration)

    _ = client.put(f"/vouchers/{'LEU123'}", cookies=cookies)

    assert voucherDB.get_voucher("LEU123").used is True


def test_handle_delete_voucher(client, cookies, config):
    voucher_codes = [
        "LEU123",
        "LEU456",
    ]
    voucher_durations = [
        "1h",
        "2h",
    ]

    voucherDB = VoucherDB(config)

    for code, duration in zip(voucher_codes, voucher_durations):
        voucherDB.add_voucher(code, duration)

    deleted_voucher = voucher_codes[1]

    _ = client.delete(
        f"http://localhost:8000/vouchers/{deleted_voucher}", cookies=cookies
    )

    with pytest.raises(KeyError):
        voucherDB.get_voucher(deleted_voucher)


# Todo add unhappy testcases
