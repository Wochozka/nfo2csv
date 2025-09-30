#!/usr/bin/env python3
import os
import csv
import xml.etree.ElementTree as ET

COLUMNS = ["OS Name", "Version", "Processor"]


def parse_xml(file_path):
    data = {f: "" for f in COLUMNS}
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        for item in root.findall(".//SystemSummary/Item"):
            name = item.findtext("Name")
            value = item.findtext("Value")
            if name in COLUMNS:
                data[name] = value
    except Exception as e:
        print(f"Chyba při zpracování {file_path}: {e}")
    return data


def main():
    # všechny xml soubory v aktuálním adresáři
    xml_files = [f for f in os.listdir(".") if f.lower().endswith(".xml")]

    rows = []
    for f in xml_files:
        parsed = parse_xml(f)
        parsed["File"] = f  # přidáme jméno souboru jako referenci
        rows.append(parsed)

    if not rows:
        print("Nenalezeny žádné XML soubory.")
        return

    # CSV sloupce: jméno souboru + vybrané položky
    fieldnames = ["File"] + COLUMNS
    with open("system_info.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Hotovo. Výstupní CSV: system_info.csv ({len(rows)} řádků)")


if __name__ == "__main__":
    main()
