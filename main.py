#!/usr/bin/env python3

import os
import csv
import xml.etree.ElementTree as ET

COLUMNS = ['Název operačního systému',
           'Verze',
           'Procesor',
           'Role platformy',
           'Název systému',
           ]


def parse_nfo(file_path):
    data = {f: "" for f in COLUMNS}
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        for item in root.findall(".//Category/Data"):
            name = item.findtext("Položka")
            value = item.findtext("Hodnota")
            if name in COLUMNS:
                data[name] = value
    except Exception as e:
        print(f"Chyba při zpracování {file_path}: {e}")
    return data


def main():
    nfo_files = [f for f in os.listdir(".") if f.lower().endswith(".nfo")]

    rows = []
    for f in nfo_files:
        parsed = parse_nfo(f)
        parsed["File"] = f
        rows.append(parsed)

    if not rows:
        print("Nenalezeny žádné nfo soubory.")
        return

    fieldnames = ["File"] + COLUMNS
    with open("system_info.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Hotovo. Výstupní CSV: system_info.csv ({len(rows)} řádků)")


if __name__ == "__main__":
    main()
