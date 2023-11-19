#!/usr/bin/env python3

import os
import re
import sys

import fitz  # pymupdf
import requests


def fetch_pdf():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    else:
        arg = os.path.expanduser("~/Downloads/AQA-8461-SP-2016.PDF")

    try:
        if arg.startswith("http"):
            response = requests.get(arg, stream=True)
            return fitz.open(stream=response.content)
        else:
            return fitz.open(filename=arg)
    except fitz.fitz.FileDataError:
        print(f"Could not open {arg}!")
        sys.exit(1)


def scan_pdf(doc):
    header_regex = re.compile(r"^(\d(?:\.\d{1,2}){0,4})\s+(.+)$", re.MULTILINE)
    for page in doc:
        text = page.get_text()
        for m in header_regex.finditer(text):
            index = m.group(1)
            title = m.group(2)
            print(f"{index:19} {title}")


if __name__ == "__main__":
    doc = fetch_pdf()
    scan_pdf(doc)
