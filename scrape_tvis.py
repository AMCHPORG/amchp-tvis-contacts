"""
TVIS MCH Director Scraper
Fetches all state/territory contacts from mchb.tvisdata.hrsa.gov
and writes two CSVs:
  - data/tvis_mch_directors.csv   (Type 1 - MCH Directors only)
  - data/tvis_all_contacts.csv    (all contact types)
"""

import csv
import json
import sys
import urllib.request
from pathlib import Path

API_URL = "https://mchb.tvisdata.hrsa.gov/api/Values/GetContactsByStateOrRegion?state=00"

TYPE_MAP = {
    1: "MCH Director",
    2: "CSHCN Director",
    3: "Family/Youth Leader",
    4: "Youth Leader",
    5: "SSDI Project Director",
}

MCH_DIRECTOR_FIELDS = [
    "StateDisplayName", "State", "Name", "Title",
    "Email", "Telephone", "Address", "RoomNumber", "City", "Zipcode",
]

ALL_CONTACT_FIELDS = [
    "StateDisplayName", "State", "ContactTypeName", "Name", "Title",
    "Email", "Telephone", "Address", "RoomNumber", "City", "Zipcode",
]


def fetch_contacts():
    req = urllib.request.Request(
        API_URL,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8")
    data = json.loads(raw)
    if not data.get("CallSuccess"):
        raise RuntimeError(f"API returned CallSuccess=false: {raw[:200]}")
    return data["result"]


def parse_contacts(result):
    all_contacts = []
    for state_group in result:
        for c in state_group:
            c["ContactTypeName"] = TYPE_MAP.get(c["Type"], f"Type {c['Type']}")
            # Normalize None -> empty string for CSV cleanliness
            for k in c:
                if c[k] is None:
                    c[k] = ""
                elif isinstance(c[k], str):
                    c[k] = c[k].strip()
            all_contacts.append(c)
    return all_contacts


def write_csv(path, fieldnames, rows):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main():
    print(f"Fetching from {API_URL} ...")
    result = fetch_contacts()
    all_contacts = parse_contacts(result)

    mch_directors = [c for c in all_contacts if c["Type"] == 1]
    mch_directors.sort(key=lambda c: c["StateDisplayName"])
    all_contacts.sort(key=lambda c: (c["StateDisplayName"], c["Order"]))

    write_csv("data/tvis_mch_directors.csv", MCH_DIRECTOR_FIELDS, mch_directors)
    write_csv("data/tvis_all_contacts.csv", ALL_CONTACT_FIELDS, all_contacts)

    print(f"✓ {len(result)} states/territories")
    print(f"✓ {len(mch_directors)} MCH Directors → data/tvis_mch_directors.csv")
    print(f"✓ {len(all_contacts)} total contacts → data/tvis_all_contacts.csv")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

