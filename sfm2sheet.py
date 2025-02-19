import sys, os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # TTK widgets
import threading
import time
import re
import pandas as pd
import json
import os
import tkinter.font as tkfont
from PIL import Image, ImageTk

###############################################################################
# 1) Define sets for certain known markers.
#    - ENTRY_MARKERS: always treated as entry-level.
#    - SENSE_MARKERS: always treated as sense-level (e.g., \sn).
###############################################################################

ENTRY_MARKERS = {
    "\\cf",  # cross reference
    "\\ct",  # complex form type
    "\\dt",  # date
    "\\ec",  # etymology comment
    "\\eg",  # etymology gloss
    "\\es",  # etymology source language notes
    "\\esl", # etymology source language
    "\\et",  # etymology source language form
    "\\hm",  # homograph number    
    "\\lc",  # citation form
    "\\lf",  # lexeme form
    "\\lt",  # literally
    "\\lv",  # lexical function lexeme
    "\\lx",  # lexeme
    "\\mn",  # main entry cross-reference
    "\\ph",  # phonemic form
    "\\se",  # subentry
    "\\va",  # variant forms
    "\\ve",  # variant comment English
    "\\vn",  # variant comment National language
    "\\vr"   # variant comment Regional language
}

SENSE_MARKERS = {
    "\\an",  # antonym
    "\\bb",  # bibliography
    "\\de",  # definition English
    "\\dn",  # definition National language
    "\\dr",  # definition Regional language
    "\\dv",  # definition Vernacular language
    "\\ee",  # encyclopedic info English
    "\\en",  # encyclopedic info National language
    "\\er",  # encyclopedic info Regional language
    "\\ev",  # encyclopedic info Vernacular language
    "\\ge",  # gloss English
    "\\gn",  # gloss National language
    "\\gr",  # gloss Regional language
    "\\gv",  # gloss Vernacular language
    "\\na",  # anthropology note
    "\\nd",  # discourse note
    "\\ng",  # grammar note
    "\\np",  # note pronunciation
    "\\nq",  # questions/notes
    "\\ns",  # sociolinguistics note
    "\\nt",  # general note
    "\\oe",  # restrictions English
    "\\on",  # restrictions National language
    "\\or",  # restrictions Regional language
    "\\ov",  # restrictions Vernacular language
    "\\ps",  # part of speech
    "\\re",  # reversal English
    "\\rf",  # reference for example sentence
    "\\rn",  # reversal National language
    "\\rr",  # reversal Regional language
    "\\sc",  # scientific name
    "\\sn",  # sense number
    "\\so",  # source
    "\\st",  # status
    "\\sy",  # synonym
    "\\ue",  # usage
    "\\xe",  # example translation English
    "\\xn",  # example translation National language
    "\\xr",  # example translation Regional language
    "\\xv"   # example sentence in Vernacular language
}

###############################################################################
# 2) Define prefixes that, if found in the marker, make it sense-level or
#    entry-level.
###############################################################################

ENTRY_PREFIXES = [
    "ea",   # e.g. \ea_Eng, \ea_Lad (etymology preceding annotations)
    "eb",   # e.g. \eb_Eng, \eb_Lad (etymology bibliography)
    "efc",  # e.g. \efc_Eng, \efc_Lad (etymology following comments)
    "eg",   # e.g. \eg_Eng, \eg_Lad (etymology gloss)
    "es",   # e.g. \es_Eng, \es_Lad (etymology source language notes)
    "et",   # e.g. \et_Eng, \et_Lad (etymology source language form)
    "v"     # e.g. \v_Eng, \v_Lad (variant comments)
]

SENSE_PREFIXES = [
    "an",   # e.g. \an_Eng, \an_Lad (antonym)
    "bb",   # e.g. \bb_Eng, \bb_Lad (bibliography)
    "d",    # e.g. \d_Eng, \d_Tib (definition)
    "e",    # e.g. \e_Eng, \e_Lad (encyclopedic info)
    "g",    # e.g. \g_Eng, \g_Hin (gloss)
    "na",   # e.g. \na_Eng, \na_Lad (anthropology note)
    "nd",   # e.g. \nd_Eng, \nd_Lad (discourse note)
    "ng",   # e.g. \ng_Eng, \ng_Lad (grammar note)
    "nq",   # e.g. \nq_Eng, \nq_Lad (questions/notes)
    "ns",   # e.g. \ns_Eng, \ns_Lad (sociolinguistics note)
    "nt",   # e.g. \nt_Eng, \nt_Lad (general note)
    "o",    # e.g. \o_Eng, \o_Lad (restrictions)
    "ps",   # e.g. \ps_Eng, \ps_Lad (part of speech)
    "r",    # e.g. \r_Eng, \r_Lad (reversal)
    "sc",   # e.g. \sc_Eng, \sc_Lad (scientific name)
    "so",   # e.g. \so_Eng, \so_Lad (source)
    "st",   # e.g. \st_Eng, \st_Lad (status)
    "sy",   # e.g. \sy_Eng, \sy_Lad (synonym)
    "u",    # e.g. \u_Eng, \u_Lad (usage)
    "x"     # e.g. \x_Eng, \x_Lad (examples)
]

###############################################################################
# 3) A helper function to decide if a marker is sense-level or entry-level.
###############################################################################

def is_sense_marker(marker: str) -> bool:
    """
    Returns True if marker is sense-level, False if entry-level.
    """
    if marker in SENSE_MARKERS:
        return True
    if marker in ENTRY_MARKERS:
        return False
    sense_pattern = r'^\\(' + '|'.join(SENSE_PREFIXES) + r')_.+'
    if re.match(sense_pattern, marker):
        return True
    entry_pattern = r'^\\(' + '|'.join(ENTRY_PREFIXES) + r')_.+'
    if re.match(entry_pattern, marker):
        return False
    return False

###############################################################################
# Conversion functions: parse_sfm, compute_max_occurrences, flatten_entries.
###############################################################################

def parse_sfm(file_path):
    """
    Parse an SFM file. Repeated occurrences of a marker are stored as a list.
    - Sense-level markers (as determined by is_sense_marker) go to the current sense.
    - Entry-level markers go to the entry-level dictionary.
    - \\sn always starts a new sense dictionary.
    """
    entries = []
    current_entry = None
    current_sense = None
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                if current_entry is not None:
                    entries.append(current_entry)
                current_entry = None
                current_sense = None
                continue

            if not line.startswith('\\'):
                continue

            parts = line.split(' ', 1)
            marker = parts[0]
            value = parts[1] if len(parts) > 1 else ""

            if current_entry is None:
                current_entry = {"lex": {}, "senses": []}
                current_sense = None

            if marker == "\\lx":
                # If we already had an entry in progress, close it out
                if current_entry and (current_entry["lex"] or current_entry["senses"]):
                    entries.append(current_entry)
                current_entry = {"lex": {}, "senses": []}
                current_sense = None
                current_entry["lex"].setdefault(marker, []).append(value)
            elif marker == "\\sn":
                current_sense = {marker: [value]}
                current_entry["senses"].append(current_sense)
            else:
                if is_sense_marker(marker):
                    if not current_entry["senses"]:
                        current_sense = {"\\sn": ["1"]}
                        current_entry["senses"].append(current_sense)
                    elif current_sense is None:
                        current_sense = {}
                        current_entry["senses"].append(current_sense)
                    current_sense.setdefault(marker, []).append(value)
                else:
                    current_entry["lex"].setdefault(marker, []).append(value)

    if current_entry and (current_entry["lex"] or current_entry["senses"]):
        entries.append(current_entry)
    return entries

def compute_max_occurrences(entries):
    """
    Determine the maximum number of occurrences for each marker at the entry level and sense level,
    plus the max number of senses across all entries.
    """
    lex_marker_occurrences = {}
    sense_marker_occurrences = {}
    max_senses = 0

    for entry in entries:
        for marker, values in entry["lex"].items():
            count = len(values)
            if count > lex_marker_occurrences.get(marker, 0):
                lex_marker_occurrences[marker] = count

        num_senses = len(entry["senses"])
        if num_senses > max_senses:
            max_senses = num_senses

        for sense in entry["senses"]:
            for marker, values in sense.items():
                count = len(values)
                if count > sense_marker_occurrences.get(marker, 0):
                    sense_marker_occurrences[marker] = count

    return lex_marker_occurrences, sense_marker_occurrences, max_senses

def flatten_entries(entries):
    """
    Flatten entries into one row per lexeme.
    Repeated markers generate repeated columns.
    For sense-level markers, repeat for each sense; the \\sn column is ensured to come first.
    """
    lex_marker_occurrences, sense_marker_occurrences, max_senses = compute_max_occurrences(entries)

    lex_markers = sorted(lex_marker_occurrences.keys())

    def sense_sort_key(m):
        return (m != '\\sn', m)
    sense_markers = sorted(sense_marker_occurrences.keys(), key=sense_sort_key)

    columns = []
    # Add columns for each lexeme-level marker
    for marker in lex_markers:
        columns += [marker] * lex_marker_occurrences[marker]

    # Add columns for sense-level markers
    for sense_index in range(1, max_senses + 1):
        for marker in sense_markers:
            columns += [f"{marker}_{sense_index}"] * sense_marker_occurrences[marker]

    rows = []
    for entry in entries:
        row_values = []
        # Fill lexeme-level columns
        for marker in lex_markers:
            needed = lex_marker_occurrences[marker]
            actual = entry["lex"].get(marker, [])
            actual += [""] * (needed - len(actual))
            row_values.extend(actual)

        # Fill sense-level columns
        for sense_index in range(max_senses):
            sense_data = entry["senses"][sense_index] if sense_index < len(entry["senses"]) else {}
            for marker in sense_markers:
                needed = sense_marker_occurrences[marker]
                actual = sense_data.get(marker, [])
                actual += [""] * (needed - len(actual))
                row_values.extend(actual)

        rows.append(row_values)

    df = pd.DataFrame(rows, columns=columns)

    # Remove numeric suffixes like _1, _2, etc.
    def remove_suffix(col):
        if "_" in col:
            base, suffix = col.rsplit("_", 1)
            if suffix.isdigit():
                return base
        return col
    df.rename(columns=remove_suffix, inplace=True)

    # FIX 1: Rename any column name that is empty (or all whitespace) to "UNKNOWN_MARKER"
    df.rename(
        columns=lambda c: c.strip() if c.strip() else "UNKNOWN_MARKER",
        inplace=True
    )

    return df

###############################################################################
# Preferences, Logging, and Global Variables
###############################################################################

CONFIG_PATH = "settings.json"

def load_settings():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {"default_font": "Arial", "last_folder": ""}

def save_settings(settings):
    with open(CONFIG_PATH, "w") as f:
        json.dump(settings, f, indent=4)

def show_preferences():
    prefs_win = tk.Toplevel(root)
    prefs_win.title("Preferences")
    prefs_win.geometry("300x200")
    settings = load_settings()

    ttk.Label(prefs_win, text="Default Font:").pack(pady=5)
    all_fonts = sorted(tkfont.families())
    font_var = tk.StringVar(value=settings.get("default_font", "Arial"))
    font_combo = ttk.Combobox(prefs_win, textvariable=font_var, values=all_fonts)
    font_combo.pack(pady=5)

    def apply_prefs():
        settings["default_font"] = font_var.get()
        save_settings(settings)
        prefs_win.destroy()

    ttk.Button(prefs_win, text="Save", command=apply_prefs).pack(pady=10)

def log_message(msg):
    log_text.config(state='normal')
    log_text.insert(tk.END, msg + "\n")
    log_text.see(tk.END)
    log_text.config(state='disabled')

# Global variables for DataFrame and suggested filename
converted_df = None
converted_filename = "output.xlsx"


###############################################################################
# Preview
###############################################################################

def show_preview(df):
    """
    Use unique column IDs for Treeview to avoid blank headings for duplicates.
    """
    for item in preview_tree.get_children():
        preview_tree.delete(item)

    cols = list(df.columns)
    unique_ids = [f"col_{i}" for i in range(len(cols))]
    preview_tree.config(columns=unique_ids, show='headings')

    for i, col_name in enumerate(cols):
        col_id = unique_ids[i]
        preview_tree.heading(col_id, text=col_name)
        preview_tree.column(col_id, width=120, anchor='center')

    preview_data = df.head(10).values.tolist()
    for row_data in preview_data:
        preview_tree.insert("", "end", values=row_data)

###############################################################################
# File Processing
###############################################################################

def process_file(file_path):
    global converted_df, converted_filename
    try:
        status_var.set(f"Parsing {os.path.basename(file_path)} ...")
        progress_bar.start()
        log_message(f"Started processing file: {file_path}")

        time.sleep(1)  # Simulate delay
        entries = parse_sfm(file_path)
        df = flatten_entries(entries)
        df.columns = [c if c.startswith("\\") else f"\\{c}" for c in df.columns]

        converted_df = df
        base = os.path.splitext(os.path.basename(file_path))[0]
        converted_filename = f"{base}.xlsx"

        def update_ui():
            notebook.select(review_frame)  # Switch to Review tab
            show_preview(df)

        root.after(0, update_ui)
        status_var.set("File processed successfully!")
        log_message("File processed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process file: {e}")
        log_message(f"Error processing file: {e}")
    finally:
        progress_bar.stop()

def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("SFM Files", "*.txt;*.sfm;*.db"), ("All Files", "*.*")]
    )
    if not file_path:
        return
    threading.Thread(target=process_file, args=(file_path,), daemon=True).start()

def on_review_save():
    if converted_df is None:
        messagebox.showwarning("No Data", "No spreadsheet data available to save.")
        return
    save_file(converted_df, initialfile=converted_filename)

def save_file(df, initialfile="output.xlsx"):
    save_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel File", "*.xlsx"), ("CSV File", "*.csv")],
        initialfile=initialfile
    )
    if save_path:
        try:
            if save_path.endswith(".csv"):
                df.to_csv(save_path, index=False)
            else:
                df.to_excel(save_path, index=False)
            messagebox.showinfo("Success", f"File saved successfully!\n{save_path}")
            status_var.set("File saved successfully!")
            log_message(f"File saved: {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")
            log_message(f"Error saving file: {e}")

###############################################################################
# About
###############################################################################

def about_link_clicked(*args):
    messagebox.showinfo(
        "About SFM2Sheet Converter",
        "SFM2Sheet Converter\n"
        "Version 1.0\n"
        "Developed by Maaz Ahmad Shaikh\n"
        "Licensed under MIT\n\n"
        "GitHub: https://github.com/SFM2SheetConverter\n"
    )

def about():
    about_win = tk.Toplevel(root)
    about_win.title("About SFM2Sheet Converter")
    about_win.geometry("400x300")
    ttk.Label(about_win, text="SFM2Sheet Converter", font=("Helvetica", 16, "bold")).pack(pady=10)
    ttk.Label(about_win, text="Version 1.0").pack()
    ttk.Label(about_win, text="Developed by [Your Name]").pack()
    ttk.Label(about_win, text="Licensed under MIT").pack(pady=10)
    ttk.Button(about_win, text="Close", command=about_win.destroy).pack(pady=10)

###############################################################################
# Build the TTK-based GUI
###############################################################################

root = tk.Tk()
root.title("SFM2Sheet Converter")
root.geometry("700x500")

style = ttk.Style()
style.theme_use('clam')

# Notebook with two tabs: Convert and Review.
notebook = ttk.Notebook(root)
convert_frame = ttk.Frame(notebook, padding="10")
review_frame = ttk.Frame(notebook, padding="10")
notebook.add(convert_frame, text="Convert")
notebook.add(review_frame, text="Review")
notebook.pack(expand=True, fill='both')


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 1) Setting the window icon and single image label
try:
    icon_path = r"C:\Users\Maaz\Documents\PythonProjects\SFM2Sheet-Converter\images\SFM2Sheet-Converter_logo.png"
    img_original = Image.open(icon_path)
    # Use LANCZOS for quality
    img_resized = img_original.resize((300, 200), Image.Resampling.LANCZOS)
    logo_img = ImageTk.PhotoImage(img_resized)
    # Set window icon
    root.iconphoto(False, logo_img)
except Exception as e:
    print("Could not load/resize icon:", e)
    logo_img = None





# Convert Tab UI

# (A) The "Open File" button at the top
ttk.Label(convert_frame, text="Select an SFM file to convert:").pack(pady=10)
open_button = ttk.Button(convert_frame, text="Open File", command=open_file)
open_button.pack(pady=10)

# Show the scaled-down image
if logo_img:
    logo_label = ttk.Label(convert_frame, image=logo_img)
    logo_label.pack(pady=10)

# **Put About link here** so it appears above the text
about_link = ttk.Label(
    convert_frame,
    text="About SFM2Sheet Converter",
    foreground="blue",
    cursor="hand2"
)
about_link.pack(pady=10)
about_link.bind("<Button-1>", about_link_clicked)

# Then the text widget
log_text = tk.Text(convert_frame, height=8, state='disabled', wrap='word')
log_text.pack(expand=False, fill='x', pady=10)

# Review Tab UI
tree_frame = ttk.Frame(review_frame)
tree_frame.pack(expand=True, fill='both')

scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal")
scrollbar_x.pack(side='bottom', fill='x')
scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical")
scrollbar_y.pack(side='right', fill='y')

preview_tree = ttk.Treeview(
    tree_frame,
    show='headings',
    xscrollcommand=scrollbar_x.set,
    yscrollcommand=scrollbar_y.set
)
preview_tree.pack(expand=True, fill='both')
scrollbar_x.config(command=preview_tree.xview)
scrollbar_y.config(command=preview_tree.yview)

ttk.Label(review_frame, text="Preview (first 10 rows):").pack()

# "Save the spreadsheet" button
save_button = ttk.Button(review_frame, text="Save the spreadsheet", command=on_review_save)
save_button.pack(pady=10)

# Font chooser
font_label = ttk.Label(review_frame, text="Choose display font:")
font_label.pack(pady=5)

all_fonts = sorted(tkfont.families())
font_var = tk.StringVar(value="Arial")
font_combo = ttk.Combobox(review_frame, textvariable=font_var, values=all_fonts, state="readonly")
font_combo.pack(pady=5)

def on_font_change(*args):
    new_font = font_var.get()
    preview_tree.configure(style="Preview.Treeview")
    style.configure("Preview.Treeview", font=(new_font, 10))

font_var.trace("w", on_font_change)

# Status bar and progress bar
status_var = tk.StringVar(value="Ready")
status_bar = ttk.Label(root, textvariable=status_var, relief='sunken', anchor='w')
status_bar.pack(side='bottom', fill='x')

progress_bar = ttk.Progressbar(root, mode='indeterminate')
progress_bar.pack(side='bottom', fill='x')

root.mainloop()