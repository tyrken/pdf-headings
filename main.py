#!/usr/bin/env python3

import os
import re
import sys

import fitz  # pymupdf
import requests

HEADER_REGEX = re.compile(r"^(\d(?:\.\d{1,2}){0,4})\s+(.+)$", re.MULTILINE)


def fetch_pdf():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    else:
        arg = os.path.expanduser(
            "~/Downloads/Geography_A_Issue3 GCSE (9-1) Specification.pdf"
        )

    try:
        if arg.startswith("http"):
            response = requests.get(arg, stream=True)
            return fitz.open(stream=response.content)
        else:
            return fitz.open(filename=arg)
    except fitz.fitz.FileDataError:
        print(f"Could not open {arg}!")
        sys.exit(1)


def display_numeric_headers(text):
    if not text:
        return
    text = text.replace("\n", " ")
    for m in HEADER_REGEX.finditer(text):
        index = m.group(1)
        title = m.group(2)
        print(f"{index:19}\t{title}")


def scan_text(doc):
    for page in doc:
        text = page.get_text()
        display_numeric_headers(text)


def scan_tables(doc):
    for page in doc:
        # if page.number < 9:
        #     continue
        # if page.number > 20:
        #     break
        tabs = page.find_tables()
        # print(f"{len(tabs.tables)} table(s) on {page}")
        for tab in tabs:
            for row in tab.extract():
                # print(row)
                for field in row:
                    display_numeric_headers(field)


if __name__ == "__main__":
    doc = fetch_pdf()
    scan_tables(doc)
