import csv
import os
import re
from io import BytesIO, StringIO

from pypdf import PdfReader


def parse_vouchers_file(file_name: str, file_contents=None) -> list[tuple[str, str]]:
    _, file_ext = os.path.splitext(file_name)
    match file_ext.lower():
        case ".pdf":
            return parse_vouchers_pdf(file_name, file_contents)
        case ".csv":
            return parse_vouchers_csv(file_name, file_contents)
        case _:
            raise ValueError(f"File extension {file_ext} not supported")


def parse_vouchers_csv(file_name: str, file_contents=None) -> list[tuple[str, str]]:
    vouchers_input = []

    if file_contents:
        text_content = file_contents.decode("utf-8")
        csv_reader = csv.reader(StringIO(text_content))
        for line in csv_reader:
            code, duration = line[0].strip().split(";")
            vouchers_input.append((code, duration))
    else:
        with open(file_name, "r") as f:
            for line in f:
                code, duration = line.strip().split(";")
                vouchers_input.append((code, duration))

    return vouchers_input


def parse_vouchers_pdf(file_name: str, file_contents=None) -> list[tuple[str, str]]:
    if file_contents:
        reader = PdfReader(BytesIO(file_contents))
    else:
        reader = PdfReader(file_name)

    # Codes and the "N uur" duration can land on different pages (the duration
    # sits in the header above the address block), so scan the whole document
    # for both rather than assuming a fixed page or an adjacent line.
    voucher_codes: list[str] = []
    duration_text: str | None = None

    for page in reader.pages:
        text = page.extract_text()
        if text is None:
            continue

        if duration_text is None:
            match = re.search(r"([0-9]+)\suur", text)
            if match is not None:
                duration_text = match.group(1)

        voucher_codes.extend(re.findall(r"LEU[A-Z_0-9]{2,}", text))

    if not voucher_codes:
        raise ValueError("No voucher codes could be read from file")

    if duration_text is None:
        raise ValueError("Duration could not be read from file")

    return [
        (code, convert_duration_text(f"{duration_text} uur")) for code in voucher_codes
    ]


def convert_duration_text(text: str) -> str:
    match text:
        case "1 uur":
            return "1h"
        case "2 uur":
            return "2h"
        case "4 uur":
            return "4h"
        case "12 uur":
            return "12h"
        case _:
            raise ValueError(f"Duration {text} does not exists")
