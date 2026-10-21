from voucher.helper import parse_vouchers_file


def test_parse_vouchers_file_csv(tmp_path):
    vouchers = [
        ("LEU121", "1h"),
        ("LEU122", "2h"),
        ("LEU123", "12h"),
        ("LEU124", "4h"),
        ("LEU125", "1h"),
        ("LEU126", "4h"),
        ("LEU127", "2h"),
        ("LEU128", "1h"),
    ]

    csv_file = tmp_path / "test_handle_add_voucher_bulk.csv"
    csv_file.write_text("".join(f"{voucher[0]};{voucher[1]}\n" for voucher in vouchers))

    assert parse_vouchers_file(str(csv_file)) == vouchers


def test_handle_add_vouchers_pdf():
    voucher_codes = [
        "LEU2CRPG36K",
        "LEU2CRPGPS3",
        "LEU2CRPGWAH",
        "LEU2CRPGGE9",
        "LEU2CRPGXKW",
        "LEU2CRPGLFU",
        "LEU2CRPG2F2",
        "LEU2CRPGHSL",
        "LEU2CRPGUR5",
        "LEU2CRPGVD3",
    ]
    duration = "2h"

    vouchers = [(code, duration) for code in voucher_codes]

    assert parse_vouchers_file("tests/data/test_vouchers.pdf") == vouchers
