# PassGuard

PassGuard is a Python-based password security toolkit created as a class exercise for Python programming. It provides a simple graphical user interface (GUI) for checking password strength, generating secure passwords, hashing passwords, and viewing a saved history of password checks.

## Project description

This repository contains a single Python application, `passguard.py`, that demonstrates practical password security concepts in a user-friendly way. The app is built using Python's built-in `tkinter` library for the interface.

## Features

- Password strength checker
  - Evaluates length, uppercase/lowercase letters, numbers, and symbols
  - Rates passwords as weak, medium, or strong
  - Provides improvement tips
- Strong password generator
  - Generates random passwords with a user-selected length
  - Ensures generated passwords meet strong-security criteria
- Password hashing
  - Uses SHA-256 to create a secure hash of a password
- Password history log
  - Saves password check results with a partial hash for reference
  - Keeps a simple local log file named `passguard_log.txt`
- User-friendly GUI
  - Built with `tkinter`
  - Includes show/hide password toggle, copy feature, and use-generated-password option

## Repository contents

- `passguard.py` — main application file containing the GUI and password security logic

## Requirements

- Python 3.x
- Tkinter (usually included with Python installations)

## How to run

From the repository folder, run:

```bash
python passguard.py
```

If your system uses `python3` instead:

```bash
python3 passguard.py
```

## Notes

- The application stores a partial hash of password checks in `passguard_log.txt` instead of saving the actual password.
- This project is intended as a learning example and demonstrates basic security practices in a simple desktop app.

## Author

- Glover Tyrese Kena
- Index No: 2526403554

## License

This repository does not currently include a formal license file. Please check with the repository owner before using the project in a production or commercial context.
