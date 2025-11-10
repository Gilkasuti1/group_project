#!/usr/bin/env python3
"""
students_report.py
Task 7 — JSON to CSV student report generator.

Reads students.json, computes averages (rounded to 2 decimals),
sorts descending by average, and writes report.csv.

Usage:
    python3 students_report.py
"""

import json
import csv
from statistics import mean

INPUT_JSON = "students.json"
OUTPUT_CSV = "report.csv"

def read_students_json(filepath):
    """Read JSON and return list of student dictionaries or None on failure."""
    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, list):
            print(f"Error: expected a JSON array in '{filepath}'.")
            return None
        return data
    except FileNotFoundError:
        print(f"Error: '{filepath}' not found. Please place students.json in the same folder.")
        return None
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON format in '{filepath}': {exc}")
        return None
    except Exception as exc:
        print(f"Unexpected error reading '{filepath}': {exc}")
        return None

def compute_averages(students):
    """
    For each student dict compute average of 'scores' (list).
    Return list of dicts: {"id":..., "name":..., "average":...}
    """
    report = []
    for s in students:
        sid = s.get("id", "")
        name = s.get("name", "")
        scores = s.get("scores", [])
        try:
            if not scores:
                avg = 0.0
            else:
                avg = round(float(mean(scores)), 2)
        except Exception:
            avg = 0.0
        report.append({"id": sid, "name": name, "average": avg})
    return report

def write_report_csv(report_rows, out_path):
    """Write rows (list of dicts) to CSV sorted by average descending."""
    sorted_rows = sorted(report_rows, key=lambda r: r["average"], reverse=True)
    try:
        with open(out_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=["id", "name", "average"])
            writer.writeheader()
            for row in sorted_rows:
                writer.writerow(row)
        print(f"Report written to '{out_path}'.")
    except Exception as exc:
        print(f"Failed to write '{out_path}': {exc}")

def main():
    print("=== students_report.py ===")
    students = read_students_json(INPUT_JSON)
    if students is None:
        return
    report_rows = compute_averages(students)
    write_report_csv(report_rows, OUTPUT_CSV)

if __name__ == "__main__":
    main()
