# Python File Management and Data Processing Utility

## Overview
This repository contains two Python scripts for the INTE 472 group project:

- `file_manager.py` — implements Tasks 1–6:
  - Creates `StudentFiles` folder (if missing).
  - Prompts for five student names and writes them into `records_YYYY-MM-DD.txt`.
  - Displays file contents, size, and last modified date.
  - Creates a backup `backup_records_YYYY-MM-DD.txt` and moves it to `StudentFiles/Archive`.
  - Logs actions in `StudentFiles/activity_log.txt`.
  - Allows optional deletion of a file and logs deletions.

- `students_report.py` — implements Task 7:
  - Reads `students.json`.
  - Computes each student's average score (rounded to 2 decimals).
  - Writes `report.csv` (columns: id, name, average), sorted by average descending.
  - Handles missing or malformed `students.json` gracefully.

## Files
- `file_manager.py`
- `students_report.py`
- `students.json` (sample)
- `README.md`

## How to run
1. Make sure Python 3.6+ is installed.
2. Place all files in the same folder.
3. Run main utility:
   ```bash
   python3 file_manager.py
