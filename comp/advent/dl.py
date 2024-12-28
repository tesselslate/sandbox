#!/usr/bin/python

import os, sys
from datetime import date
from urllib.request import urlopen, Request

os.makedirs("inputs", exist_ok=True)

year = os.path.basename(os.getcwd())
try:
    year = int(year)
except:
    print("Invalid directory")

TOKEN = open("../.aoc_token").read().strip("\n")

days = set()
for arg in sys.argv[1:]:
    if arg.isdigit():
        day = int(arg)
        if day in days:
            print("Cannot download same day twice")
        days.add(day)
    elif arg == "all":
        if input("Download all days? (y/n): ").startswith("y"):
            for day in range(1, 26):
                days.add(day)
        else:
            exit(1)
    else:
        print("Invalid argument")
        exit(1)
if not days:
    today = date.today()

    if today.month != 12 or today.day > 25:
        print(f"Invalid date ({today}) for auto-download")
        exit(1)

    days.add(today.day)

days = list(sorted(days))

for day in days:
    filename = f"inputs/{str(day).zfill(2)}"
    url = f"https://adventofcode.com/{year}/day/{str(day)}/input"
    headers = {
        "Cookie": f"session={TOKEN}",
        "User-Agent": "github.com/tesselslate",
    }

    print(f"Downloading {day}...")

    req = Request(url, headers=headers)
    with urlopen(req) as resp:
        data = resp.read().decode("utf-8")
        with open(filename, "w") as file:
            file.write(data)

        data_sz = len(data)
        data_lines = data.count("\n")
        data_blocks = len(data.split("\n\n"))
        print(f"Done! {data_sz} bytes | {data_lines} lines | {data_blocks} blocks")
