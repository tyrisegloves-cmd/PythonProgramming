"""
PassGuard
A Password Security Toolkit (GUI)
Lab 1 Python (Level 200)
Author: Glover Tyrese Kena | Index No: 2526403554
"""

import string
import secrets
import hashlib
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

LOG_FILE = "passguard_log.txt"

COMMON_PASSWORDS = [
    "123456", "password", "123456789", "12345678", "12345",
    "qwerty", "abc123", "111111", "123123", "admin",
    "letmein", "welcome", "iloveyou", "monkey", "football",
    "password1", "000000", "ghana123", "accra123", "god123",
]

COLOURS = {
    "VERY WEAK": "#b71c1c",
    "WEAK": "#e53935",
    "MEDIUM": "#fb8c00",
    "STRONG": "#2e7d32"
}


# -------------------------------------Logic functions (no GUI code here)------------------------------------------------

def check_strength(password):
    """Return (score, label, tips) for a password."""
    score = 0
    tips = []

    if password.lower() in COMMON_PASSWORDS:
        return 0, "VERY WEAK", ["This is one of the most common passwords. Never use it."]

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
        tips.append("Use 12 or more characters for extra strength.")
    else:
        tips.append("Too short. Use at least 8 characters (12+ is better).")

    if any(ch.isupper() for ch in password):
        score += 1
    else:
        tips.append("Add an uppercase letter (A-Z).")

    if any(ch.islower() for ch in password):
        score += 1
    else:
        tips.append("Add a lowercase letter (a-z).")

    if any(ch.isdigit() for ch in password):
        score += 1
    else:
        tips.append("Add a number (0-9).")

    if any(ch in string.punctuation for ch in password):
        score += 1
    else:
        tips.append("Add a symbol such as ! @ # $ %.")

    if score <= 2:
        label = "WEAK"
    elif score <= 4:
        label = "MEDIUM"
    else:
        label = "STRONG"

    return score, label, tips


def generate_password(length=16):
    """Generate a random password that is always STRONG."""
    if length < 8:
        length = 8
    all_chars = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = "".join(secrets.choice(all_chars) for _ in range(length))
        score, label, tips = check_strength(password)
        if label == "STRONG":
            return password


def hash_password(password):
    """Return the SHA-256 hash of a password as hex text."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def save_to_log(password, score, label):
    """Save a check. Only part of the HASH is stored, never the password."""
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    short_hash = hash_password(password)[:10]
    record = f"{time_now} | {short_hash}... | {score}/6 | {label}"
    with open(LOG_FILE, "a") as file:
        file.write(record + "\n")
    return record


def load_log():
    """Return a list of saved records (empty list if no file yet)."""
    try:
        with open(LOG_FILE, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []


# -------------------------------------------GUI event handlers-----------------------------------------------------------------

def live_check(event=None):
    """Update the strength bar every time a key is pressed."""
    password = password_entry.get()
    if password == "":
        strength_bar["value"] = 0
        result_label.config(text="Start typing a password...", fg="grey")
        tips_label.config(text="")
        return
    score, label, tips = check_strength(password)
    strength_bar["value"] = score
    result_label.config(text=f"{label} ({score}/6)", fg=COLOURS[label])
    tips_label.config(text="\n".join("- " + tip for tip in tips))


def on_check():
    password = password_entry.get()
    if password == "":
        messagebox.showwarning("PassGuard", "Please type a password first.")
        return
    score, label, tips = check_strength(password)
    record = save_to_log(password, score, label)
    history_list.insert(tk.END, record)
    messagebox.showinfo("PassGuard", f"Result: {label} ({score}/6)\nSaved to history.")


def toggle_show():
    if show_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")


def on_generate():
    new_password = generate_password(length_var.get())
    generated_var.set(new_password)


def on_copy():
    root.clipboard_clear()
    root.clipboard_append(generated_var.get())
    messagebox.showinfo("PassGuard", "Password copied to clipboard.")


def on_use_generated():
    """Extension #2: Copy generated password into check entry and trigger live_check."""
    generated_pwd = generated_var.get()
    if not generated_pwd:
        messagebox.showwarning("PassGuard", "Please generate a password first.")
        return

    # Fill the password check box
    password_entry.delete(0, tk.END)
    password_entry.insert(0, generated_pwd)

    # Check 'Show password' box so it's visible to the user
    show_var.set(True)
    toggle_show()

    # Run the live check evaluation
    live_check()


def on_hash():
    password = password_entry.get()
    if password == "":
        messagebox.showwarning("PassGuard", "Please type a password first.")
        return
    hash_var.set(hash_password(password))


# ------------------------------------------Build the window--------------------------------------------

root = tk.Tk()
root.title("PassGuard - Password Security Toolkit")
root.geometry("560x670")
root.resizable(False, False)

title_label = tk.Label(root, text="PassGuard", font=("Segoe UI", 22, "bold"), fg="#0d47a1")
title_label.pack(pady=(15, 0))
tk.Label(root, text="Check, generate and hash passwords safely").pack()

# Section 1: Check strength
check_frame = tk.LabelFrame(root, text=" 1. Check password strength ", padx=10, pady=10)
check_frame.pack(fill="x", padx=15, pady=10)

password_entry = tk.Entry(check_frame, show="*", font=("Segoe UI", 12), width=35)
password_entry.pack(fill="x")
password_entry.bind("<KeyRelease>", live_check)

show_var = tk.BooleanVar()
tk.Checkbutton(check_frame, text="Show password", variable=show_var, command=toggle_show).pack(anchor="w")

strength_bar = ttk.Progressbar(check_frame, maximum=6, length=400)
strength_bar.pack(fill="x", pady=5)

result_label = tk.Label(check_frame, text="Start typing a password...", font=("Segoe UI", 12, "bold"), fg="grey")
result_label.pack(anchor="w")

tips_label = tk.Label(check_frame, text="", justify="left", fg="#444")
tips_label.pack(anchor="w")

button_row = tk.Frame(check_frame)
button_row.pack(anchor="w", pady=(5, 0))

tk.Button(button_row, text="Save check", command=on_check, width=12).pack(side="left")
tk.Button(button_row, text="Hash it", command=on_hash, width=12).pack(side="left", padx=5)

hash_var = tk.StringVar()
tk.Entry(check_frame, textvariable=hash_var, state="readonly", font=("Consolas", 8)).pack(fill="x", pady=(5, 0))

# Section 2: Generate
gen_frame = tk.LabelFrame(root, text=" 2. Generate a strong password ", padx=10, pady=10)
gen_frame.pack(fill="x", padx=15, pady=5)

gen_row1 = tk.Frame(gen_frame)
gen_row1.pack(fill="x", pady=(0, 5))

tk.Label(gen_row1, text="Length:").pack(side="left")
length_var = tk.IntVar(value=16)
tk.Spinbox(gen_row1, from_=8, to=32, width=4, textvariable=length_var, state="readonly").pack(side="left", padx=5)
tk.Button(gen_row1, text="Generate", command=on_generate).pack(side="left", padx=5)

generated_var = tk.StringVar()
tk.Entry(gen_row1, textvariable=generated_var, state="readonly", font=("Consolas", 11), width=22).pack(side="left",
                                                                                                       padx=5)

gen_row2 = tk.Frame(gen_frame)
gen_row2.pack(fill="x")

tk.Button(gen_row2, text="Copy", command=on_copy, width=10).pack(side="left", padx=(0, 5))
tk.Button(gen_row2, text="Use password", command=on_use_generated, width=14).pack(side="left")

# Section 3: History
hist_frame = tk.LabelFrame(root, text=" 3. Check history (hashes only) ", padx=10, pady=10)
hist_frame.pack(fill="both", expand=True, padx=15, pady=10)

history_list = tk.Listbox(hist_frame, font=("Consolas", 9), height=8)
history_list.pack(fill="both", expand=True)

for saved_record in load_log():
    history_list.insert(tk.END, saved_record)

root.mainloop()