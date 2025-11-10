#!/usr/bin/env python3
"""
file_manager.py
INTE 472 - Scripting Languages
Rewritten complete implementation of Tasks 1-6.

Usage:
    python3 file_manager.py
Optional (non-interactive) flags could be added if desired.
"""

import os
import sys
import shutil
from datetime import datetime

STUDENT_FOLDER = "StudentFiles"
ARCHIVE_FOLDER_NAME = "Archive"
LOG_FILENAME = "activity_log.txt"

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ---------------------------
# Task 1 - Initialization
# ---------------------------
def init_student_folder():
    """
    Ensure the StudentFiles folder exists. Return its absolute path.
    On failure, log and exit using sys.exit().
    """
    try:
        if not os.path.exists(STUDENT_FOLDER):
            os.makedirs(STUDENT_FOLDER)
            print(f"Created folder: {os.path.abspath(STUDENT_FOLDER)}")
        else:
            print(f"Folder already exists: {os.path.abspath(STUDENT_FOLDER)}")
        return os.path.abspath(STUDENT_FOLDER)
    except Exception as exc:
        # Try to write error into local log if possible, then exit
        try:
            with open(LOG_FILENAME, "a", encoding="utf-8") as lf:
                lf.write(f"[{timestamp()}] ERROR: Failed to create '{STUDENT_FOLDER}': {exc}\n")
        except Exception:
            pass
        sys.exit(f"Fatal: could not create or access '{STUDENT_FOLDER}': {exc}")

# ---------------------------
# Task 5 Helpers - Logging
# ---------------------------
def log_info(message):
    """Append a timestamped info message to StudentFiles/activity_log.txt."""
    entry = f"[{timestamp()}] {message}\n"
    try:
        with open(os.path.join(STUDENT_FOLDER, LOG_FILENAME), "a", encoding="utf-8") as lf:
            lf.write(entry)
    except Exception:
        # fallback to local directory
        with open(LOG_FILENAME, "a", encoding="utf-8") as lf:
            lf.write(entry)

def log_error(message):
    """Append a timestamped error message to StudentFiles/activity_log.txt."""
    entry = f"[{timestamp()}] ERROR: {message}\n"
    try:
        with open(os.path.join(STUDENT_FOLDER, LOG_FILENAME), "a", encoding="utf-8") as lf:
            lf.write(entry)
    except Exception:
        with open(LOG_FILENAME, "a", encoding="utf-8") as lf:
            lf.write(entry)

# ---------------------------
# Task 2 - File creation & writing
# ---------------------------
def generate_records_filename(for_date=None):
    """Return filename like records_YYYY-MM-DD.txt using given date or today."""
    if for_date is None:
        for_date = datetime.now()
    date_part = for_date.strftime("%Y-%m-%d")
    return f"records_{date_part}.txt"

def write_student_records(folder_path, names):
    """
    Write the provided list of names (strings) to the date-named file inside folder_path.
    Returns the full path to the file written.
    """
    filename = generate_records_filename()
    full_path = os.path.join(folder_path, filename)
    try:
        with open(full_path, "w", encoding="utf-8") as fh:
            for name in names:
                fh.write(f"{name}\n")
        created_at = timestamp()
        print(f"File written: {filename} at {created_at}")
        log_info(f"{filename} created successfully.")
        return full_path
    except Exception as exc:
        print(f"Error: could not write file '{filename}': {exc}")
        log_error(f"Failed to write '{filename}': {exc}")
        return None

# ---------------------------
# Task 3 - Read & file info
# ---------------------------
def display_file_contents_and_info(file_path):
    """Read and print file contents, size in bytes, and last modified datetime."""
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            content = fh.read()
        print("\n--- File contents ---")
        print(content.strip() or "(empty file)")
    except Exception as exc:
        print(f"Error reading file '{file_path}': {exc}")
        log_error(f"Failed to read '{file_path}': {exc}")
        return

    try:
        size = os.path.getsize(file_path)
        mtime = os.path.getmtime(file_path)
        mdate = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        print(f"Size: {size} bytes")
        print(f"Last modified: {mdate}")
    except Exception as exc:
        print(f"Error retrieving metadata for '{file_path}': {exc}")
        log_error(f"Failed to get metadata for '{file_path}': {exc}")

# ---------------------------
# Task 4 - Backup & Archive
# ---------------------------
def backup_and_archive_file(file_path, folder_path):
    """
    Copy the file to a backup file backup_<originalname> and move it into Archive subfolder.
    List files in archive afterwards.
    """
    try:
        base_name = os.path.basename(file_path)
        backup_name = f"backup_{base_name}"
        backup_path = os.path.join(folder_path, backup_name)
        shutil.copy(file_path, backup_path)
        print(f"Backup created: {backup_name}")
    except Exception as exc:
        print(f"Error creating backup for '{file_path}': {exc}")
        log_error(f"Failed to create backup for '{file_path}': {exc}")
        return

    archive_folder = os.path.join(folder_path, ARCHIVE_FOLDER_NAME)
    try:
        if not os.path.exists(archive_folder):
            os.makedirs(archive_folder)
            print(f"Created archive folder: {archive_folder}")
    except Exception as exc:
        print(f"Error creating archive folder '{archive_folder}': {exc}")
        log_error(f"Failed to create archive folder '{archive_folder}': {exc}")
        return

    try:
        moved = shutil.move(backup_path, archive_folder)
        moved_name = os.path.basename(moved)
        print(f"Backup moved to Archive: {moved_name}")
        # List files in Archive
        archive_files = os.listdir(archive_folder)
        print("\nFiles in Archive:")
        for f in archive_files:
            print(f"- {f}")
        log_info(f"{base_name} created and archived successfully.")
    except Exception as exc:
        print(f"Error moving backup to archive: {exc}")
        log_error(f"Failed to move backup '{backup_path}' to '{archive_folder}': {exc}")

# ---------------------------
# Task 6 - Advanced file ops (delete)
# ---------------------------
def prompt_and_delete_file(folder_path):
    """
    Ask user whether to delete a file. If yes, delete specified file and log.
    Always display remaining files in the StudentFiles folder afterwards.
    """
    try:
        answer = input("\nWould you like to delete a file from the StudentFiles folder? (Yes/No): ").strip().lower()
    except KeyboardInterrupt:
        print("\nInput cancelled by user.")
        return

    if answer in ("yes", "y"):
        fname = input("Enter filename to delete (include extension): ").strip()
        target = os.path.join(folder_path, fname)
        if not os.path.exists(target):
            print(f"File not found: {fname}")
            log_error(f"Deletion attempted for missing file: {fname}")
        else:
            try:
                os.remove(target)
                print(f"Deleted file: {fname}")
                log_info(f"{fname} deleted by user.")
            except Exception as exc:
                print(f"Error deleting file '{fname}': {exc}")
                log_error(f"Failed to delete '{fname}': {exc}")
    else:
        print("No deletion performed.")

    # Display remaining files in StudentFiles (top level)
    try:
        files = os.listdir(folder_path)
        print("\nRemaining files in StudentFiles:")
        for f in files:
            print(f"- {f}")
    except Exception as exc:
        print(f"Could not list files in '{folder_path}': {exc}")
        log_error(f"Failed to list files in '{folder_path}': {exc}")

# ---------------------------
# Utility - get 5 student names interactively
# ---------------------------
def get_five_student_names():
    """Prompt the user to enter five student names; returns list of 5 names."""
    print("\nPlease enter five student names (press Enter to accept default).")
    names = []
    for i in range(1, 6):
        try:
            n = input(f"Student {i} name: ").strip()
        except KeyboardInterrupt:
            print("\nInput interrupted; using defaults for remaining students.")
            n = ""
        if not n:
            n = f"Student_{i}"
        names.append(n)
    return names

# ---------------------------
# Main
# ---------------------------
def main():
    print("=== Python File Management Utility (Tasks 1-6) ===")
    folder_path = init_student_folder()
    # Get student names and write file
    names = get_five_student_names()
    file_path = write_student_records(folder_path, names)
    if not file_path:
        sys.exit("Exiting due to file creation error.")
    display_file_contents_and_info(file_path)
    backup_and_archive_file(file_path, folder_path)
    prompt_and_delete_file(folder_path)
    print("\nDone. Check activity_log.txt inside the StudentFiles folder for log entries.")

if __name__ == "__main__":
    main()
