import io
from unittest.mock import patch

import pytest

from cli import repl
from cli.handlers.help import handle_help
from cli.handlers.user import handle_manage_user
from cli.handlers.voucher import (
    handle_add_voucher,
    handle_add_vouchers_file,
    handle_list_vouchers,
    handle_use_voucher,
)
from db.models import Voucher
from voucher.models import VoucherDB


def test_handle_help(config):
    with patch("sys.stdout", new=io.StringIO()) as dummy_stdout:
        handle_help(config)

        output = dummy_stdout.getvalue().strip()
        assert "help" in output
        assert "exit" in output
        assert "list" in output
        assert "add" in output
        assert "add-file" in output
        assert "add-user" in output
        # "use" was missing from the old hardcoded help text.
        assert "use" in output


def test_handle_help_lists_every_registered_command(config):
    from cli import clicommands

    with patch("sys.stdout", new=io.StringIO()) as dummy_stdout:
        handle_help(config)

        output = dummy_stdout.getvalue()

    for command in clicommands.get_commands():
        assert command in output


def test_handle_add_voucher(config):
    vouch = Voucher("LEU123", "1h")

    with patch("cli.handlers.voucher.input") as mock_input:
        mock_input.side_effect = [vouch.code, "a"]
        handle_add_voucher(config)

    voucherDB = VoucherDB(config)

    expected_vouch = Voucher("LEU123", "1h")
    assert voucherDB.get_voucher(expected_vouch.code) == expected_vouch


def test_handle_add_vouchers_file_csv(config, tmp_path):
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
    csv_file.write_text("".join(f"{code};{duration}\n" for code, duration in vouchers))

    with patch("cli.handlers.voucher.input") as mock_input:
        mock_input.side_effect = [str(csv_file)]
        handle_add_vouchers_file(config)

    voucherDB = VoucherDB(config)
    expected_vouchers = [Voucher(code, duration) for code, duration in vouchers]

    assert voucherDB.get_vouchers() == expected_vouchers


# Todo add unhappy testcases


def test_handle_add_vouchers_file_pdf(config):
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

    with patch("cli.handlers.voucher.input") as mock_input:
        mock_input.side_effect = ["tests/data/test_vouchers.pdf"]
        handle_add_vouchers_file(config)

    voucherDB = VoucherDB(config)
    expected_vouchers = []
    for code in voucher_codes:
        expected_vouchers.append(Voucher(code, duration))

    assert voucherDB.get_vouchers() == expected_vouchers


def test_handle_list_voucher(config):
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

    expected_vouch = Voucher("LEU123", "1h")
    expected_vouch2 = Voucher("LEU456", "2h")

    with patch("sys.stdout", new=io.StringIO()) as dummy_stdout:
        handle_list_vouchers(config)

        output = dummy_stdout.getvalue().strip()
        assert expected_vouch.code in output
        assert expected_vouch2.code in output


def test_handle_use_voucher(config):
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

    handle_use_voucher(config, "LEU123")

    assert voucherDB.get_voucher("LEU123").used is True


def test_handle_use_voucher_prints_success(config, capsys):
    voucherDB = VoucherDB(config)
    voucherDB.add_voucher("LEU123", "1h")

    handle_use_voucher(config, "LEU123")

    assert "LEU123" in capsys.readouterr().out
    assert voucherDB.get_voucher("LEU123").used is True


def test_handle_use_voucher_already_used_message(config, capsys):
    voucherDB = VoucherDB(config)
    voucherDB.add_voucher("LEU123", "1h")
    voucherDB.use_voucher("LEU123")

    handle_use_voucher(config, "LEU123")

    assert "already used" in capsys.readouterr().out


def test_handle_use_voucher_unknown_code_message(config, capsys):
    handle_use_voucher(config, "LEU666")

    assert "does not exist" in capsys.readouterr().out


def test_handle_add_voucher_rejects_empty_code(config, capsys):
    with patch("builtins.input", return_value=""):
        handle_add_voucher(config)

    assert "voucher code required" in capsys.readouterr().out
    assert VoucherDB(config).get_vouchers() == []


def test_handle_add_vouchers_file_unsupported_extension(config, tmp_path, capsys):
    bad_file = tmp_path / "vouchers.txt"
    bad_file.write_text("LEU121;1h\n")

    with patch("builtins.input", return_value=str(bad_file)):
        handle_add_vouchers_file(config)

    out = capsys.readouterr().out
    assert "not supported" in out
    assert VoucherDB(config).get_vouchers() == []


def test_handle_add_vouchers_file_missing_file_message(config, tmp_path, capsys):
    with patch("builtins.input", return_value=str(tmp_path / "nope.pdf")):
        handle_add_vouchers_file(config)

    assert "File not found" in capsys.readouterr().out


def test_handle_manage_user_unknown_user_message(config, capsys):
    with patch("builtins.input", return_value="nobody"):
        handle_manage_user(config)

    assert "does not exist" in capsys.readouterr().out


def _run_repl(config, lines):
    """Drive the REPL with the given input lines until it exits.

    Every session ends via handle_exit, so SystemExit is the expected outcome.
    """
    with (
        patch("builtins.input", side_effect=lines),
        pytest.raises(SystemExit) as excinfo,
    ):
        repl.start(config)

    return excinfo.value.code


def test_repl_exits_cleanly_on_eof(config, capsys):
    """Ctrl-D must end the session, not surface an EOFError traceback."""
    exit_code = _run_repl(config, EOFError)

    assert exit_code == 0
    assert "Exiting application" in capsys.readouterr().out


def test_repl_exits_cleanly_on_interrupt(config, capsys):
    exit_code = _run_repl(config, KeyboardInterrupt)

    assert exit_code == 0
    assert "Exiting application" in capsys.readouterr().out


def test_repl_ignores_empty_input(config, capsys):
    _run_repl(config, ["", "   ", EOFError])

    assert "command unknown" not in capsys.readouterr().out


def test_repl_reports_unknown_command(config, capsys):
    _run_repl(config, ["bogus", EOFError])

    assert "command unknown" in capsys.readouterr().out


def test_repl_dispatches_command_with_args(config, capsys):
    voucherDB = VoucherDB(config)
    voucherDB.add_voucher("LEU123", "1h")

    _run_repl(config, ["use leu123", EOFError])

    out = capsys.readouterr().out
    assert "Used voucher" in out
    assert voucherDB.get_voucher("LEU123").used is True


def test_error_message_unquotes_keyerror():
    from cli.errors import error_message

    # KeyError.__str__ adds quotes; the CLI should not show them.
    assert error_message(KeyError("Voucher does not exist")) == "Voucher does not exist"


def test_error_message_keeps_valueerror_text():
    from cli.errors import error_message

    assert error_message(ValueError("Voucher was already used")) == (
        "Voucher was already used"
    )


def test_error_message_stringifies_non_string_args():
    from cli.errors import error_message

    assert error_message(KeyError(123)) == "123"


def test_error_message_handles_empty_keyerror():
    from cli.errors import error_message

    # str(KeyError()) is "" - the caller still gets something printable.
    assert error_message(KeyError()) == ""
