#!/usr/bin/env python3

import re
import sys
from pprint import pprint  # noqa

import fitz  # pymupdf
import requests


def fetch_pdf():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    else:
        print("You must provide an input argument to parse!", file=sys.stderr)
        sys.exit(1)

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
    regex = re.compile(r"^(\d(?:\.\d{1,2}){1,4})\s+(.+)$", re.MULTILINE)
    # text = text.replace("\n", " ")
    for m in regex.finditer(text):
        index = m.group(1)
        title = m.group(2)
        if title.startswith("– "):
            title = title[2:]
        print(f"{index:19}\t{title}")


def display_alnum_headers(text):
    HEADER_REGEX = re.compile(r"^([A-Z]\d{1,2})\s+(.+)$", re.MULTILINE)
    if not text:
        return
    # text = text.replace("\n", " ")
    for m in HEADER_REGEX.finditer(text):
        index = m.group(1)
        title = m.group(2)
        print(f"{index:19}\t{title}")


def split_alnum_lines(text):
    def grab(header: str, body: str):
        body = body.strip()
        body = body[0].upper() + body[1:]
        print(f"{header:7}\t{body}")

    if not text:
        return

    regex = re.compile(r"([A-Z]\d{1,2}) ", re.MULTILINE)
    text = text.replace("\n", " ")
    last_endpos = None
    last_header = None
    # print(f"------\n{text}\n======")
    for m in regex.finditer(text):
        # print(m)
        if last_endpos:
            body = text[last_endpos : m.start()]
            grab(last_header, body)
        last_endpos = m.end()
        last_header = m.group(1)
    if last_endpos:
        body = text[last_endpos:]
        grab(last_header, body)


def scan_text(page):
    # print(f"PAGE: {page}")
    # print()
    text = page.get_text()
    # print(text)
    display_numeric_headers(text)
    # display_alnum_headers(text)
    # split_alnum_lines(text)


def scan_tables(page):
    tabs = page.find_tables()
    print(f"{len(tabs.tables)} table(s) on {page}")
    for tab in tabs:
        for row in tab.extract():
            # print(row)
            for text in row:
                print(f">>{text}<<")
                display_numeric_headers(text)
                # display_alnum_headers(text)


def main():
    doc = fetch_pdf()
    for page in doc:
        if page.number < 5:
            continue
        # if page.number > 20:
        #     break
        # scan_tables(page)
        scan_text(page)


if __name__ == "__main__":
    main()
