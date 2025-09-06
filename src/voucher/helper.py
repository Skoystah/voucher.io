from io import BytesIO, StringIO
import os
import re
import csv
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

    text = reader.pages[2].extract_text()

    voucher_codes = re.findall(r"LEU[A-Z_0-9]{2,}", text)
    voucher_duration_text = re.search(r"[0-9]+\suur", text)
    if voucher_duration_text is None:
        raise Exception("Duration could not be read from file")

    vouchers_input = [
        (code, convert_duration_text(voucher_duration_text.group()))
        for code in voucher_codes
    ]

    return vouchers_input


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
