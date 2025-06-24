from usb_utils import get_usb_drive_by_label
import os
import shutil
import re

def toggle_enLvdsFormat(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    pattern = re.compile(r"^(enLvdsFormat)(\s*=\s*)([01])(\s*,?\s*)$")
    for i, line in enumerate(lines):
        m = pattern.match(line.strip())
        if m:
            key, eq_space, val, suffix = m.groups()
            new_val = "0" if val == "1" else "1"
            lines[i] = f"{key}{eq_space}{new_val}{suffix}\n"
            break
    else:
        raise RuntimeError("enLvdsFormat line not found in file.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

def toggle_b8Flip_lines(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    pattern = re.compile(r"^(b8HFlip|b8VFlip)(\s*=\s*)([01])(\s*,?\s*)$")
    found_h, found_v = False, False

    for i, line in enumerate(lines):
        m = pattern.match(line.strip())
        if m:
            key, eq_space, val, suffix = m.groups()
            new_val = "0" if val == "1" else "1"
            lines[i] = f"{key}{eq_space}{new_val}{suffix}\n"
            if key == "b8HFlip":
                found_h = True
            elif key == "b8VFlip":
                found_v = True

    if not (found_h and found_v):
        missing = []
        if not found_h:
            missing.append("b8HFlip")
        if not found_v:
            missing.append("b8VFlip")
        raise RuntimeError(f"Missing lines: {', '.join(missing)}")

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

def insert_blank(label, filename="downloadpq.mb211"):
    usb_drive = get_usb_drive_by_label(label)
    if not usb_drive:
        raise RuntimeError(f"USB drive with label '{label}' not found.")

    blank_file_path = os.path.join(usb_drive, filename)
    with open(blank_file_path, "w", encoding="utf-8") as f:
        pass  # Creates an empty file

    print(f"Blank file '{filename}' created on USB drive at: {blank_file_path}")

def save_pq(label):
    usb_drive = get_usb_drive_by_label(label)
    if not usb_drive:
        raise RuntimeError(f"USB drive with label '{label}' not found.")

    dvr_folder = os.path.join(usb_drive, "DVR")
    blank_file = os.path.join(usb_drive, "downloadpq.mb211")
    pq_folder = os.path.join(usb_drive, "pq")

    # Delete DVR folder if exists
    if os.path.exists(dvr_folder) and os.path.isdir(dvr_folder):
        shutil.rmtree(dvr_folder)
        print(f"Deleted folder: {dvr_folder}")

    # Delete downloadpq.mb211 file if exists
    if os.path.exists(blank_file) and os.path.isfile(blank_file):
        os.remove(blank_file)
        print(f"Deleted file: {blank_file}")

    # Create pq folder if it doesn't exist
    os.makedirs(pq_folder, exist_ok=True)

    # Move all remaining files/folders (except pq) into pq folder
    for item in os.listdir(usb_drive):
        if item == "pq":
            continue  # Skip pq folder itself
        src = os.path.join(usb_drive, item)
        dst = os.path.join(pq_folder, item)

        shutil.move(src, dst)
        print(f"Moved '{src}' -> '{dst}'")

    print("Save operation completed.")
