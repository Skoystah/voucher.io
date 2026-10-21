"""Tests for parse_vouchers_pdf.

The parser must read every page (codes and the "N uur" duration line can land
on different pages) and raise ValueError, not a bare Exception, when either is
missing. The historical implementation only read pages[2], which happened to
work for the real fixture but broke on any other layout.
"""

import io
import re

import pytest
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    DecodedStreamObject,
    DictionaryObject,
    NameObject,
)

from voucher.helper import parse_vouchers_file, parse_vouchers_pdf


def _pdf_bytes(pages: list[str]) -> bytes:
    """Render plain-text pages into an in-memory PDF.

    pypdf has no text API, so the pages are assembled by hand as content
    streams with a standard Helvetica font. That keeps the suite free of a
    PDF-writer dependency while producing documents pypdf can read back.
    """
    writer = PdfWriter()
    for text in pages:
        ops = " ".join(f"({line}) Tj T*" for line in text.split("\n"))
        stream = f"BT /F1 11 Tf 72 720 Td 14 TL {ops} ET".encode("latin-1")

        page = writer.add_blank_page(width=595, height=842)
        page[NameObject("/Resources")] = DictionaryObject(
            {
                NameObject("/Font"): DictionaryObject(
                    {
                        NameObject("/F1"): DictionaryObject(
                            {
                                NameObject("/Type"): NameObject("/Font"),
                                NameObject("/Subtype"): NameObject("/Type1"),
                                NameObject("/BaseFont"): NameObject("/Helvetica"),
                            }
                        )
                    }
                )
            }
        )
        contents = DecodedStreamObject()
        contents.set_data(stream)
        page[NameObject("/Contents")] = writer._add_object(contents)

    buffer = io.BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


def test_duration_and_codes_on_same_page():
    pdf = _pdf_bytes(["Gratis voucher 2 uur\nLEU2CRPG36K\nLEU2CRPGPS3"])

    assert parse_vouchers_pdf("x.pdf", pdf) == [
        ("LEU2CRPG36K", "2h"),
        ("LEU2CRPGPS3", "2h"),
    ]


def test_duration_on_earlier_page_than_codes():
    """The real Leuven PDF puts the duration in the header of an earlier page."""
    pdf = _pdf_bytes(
        ["Gratis voucher 4 uur\nSome address block", "LEUAAA111\nLEUBBB222"]
    )

    assert parse_vouchers_pdf("x.pdf", pdf) == [
        ("LEUAAA111", "4h"),
        ("LEUBBB222", "4h"),
    ]


def test_codes_on_earlier_page_than_duration():
    pdf = _pdf_bytes(["LEUAAA111\nLEUBBB222", "Gratis voucher 1 uur"])

    assert parse_vouchers_pdf("x.pdf", pdf) == [
        ("LEUAAA111", "1h"),
        ("LEUBBB222", "1h"),
    ]


def test_duration_missing_raises_valueerror():
    pdf = _pdf_bytes(["LEUAAA111\nLEUBBB222"])

    with pytest.raises(ValueError):
        parse_vouchers_pdf("x.pdf", pdf)


def test_codes_missing_raises_valueerror():
    pdf = _pdf_bytes(["Gratis voucher 2 uur"])

    with pytest.raises(ValueError):
        parse_vouchers_pdf("x.pdf", pdf)


def test_empty_document_raises_valueerror():
    with pytest.raises(ValueError):
        parse_vouchers_pdf("x.pdf", _pdf_bytes([""]))


def test_unsupported_extension_raises_valueerror(tmp_path):
    path = tmp_path / "vouchers.txt"
    path.write_text("whatever")

    with pytest.raises(ValueError):
        parse_vouchers_file(str(path))


def test_real_fixture_still_parses():
    vouchers = parse_vouchers_file("tests/data/test_vouchers.pdf")

    assert len(vouchers) == 10
    assert all(duration == "2h" for _, duration in vouchers)
    assert all(code.startswith("LEU") for code, _ in vouchers)


def test_real_fixture_codes_and_duration_share_a_page():
    """Documents what the fixture actually looks like, so a future layout
    change shows up here rather than as a silent mis-parse."""
    page = PdfReader("tests/data/test_vouchers.pdf").pages[2].extract_text()

    assert re.search(r"LEU2CRPG36K", page)
    assert re.search(r"2\suur", page)
