# Task 22: File Organizer 📁⚡

A clean, robust, and beginner-friendly Python automation script that scans any target directory and automatically organizes loose files into categorized subdirectories based on their file extensions.

Developed as part of the Python Internship series to demonstrate **filesystem automation**, clean architecture, defensive programming (collision handling), and standard library mastery using `pathlib` and `shutil`.

---

## 🎯 Project Overview & Goals

In real-world workflows, folders like `Downloads` or desktop spaces quickly become cluttered with hundreds of mixed files: documents, images, installers, zip archives, and scripts. Manually sorting these files is slow and error-prone.

This project solves that problem with a single command:
1. **Scans** the target folder for loose files.
2. **Maps** extensions to clean categories (`Documents`, `Images`, `Videos`, `Audio`, `Archives`, `Code`, `Others`).
3. **Creates folders dynamically** (only creating folders when matching files exist).
4. **Protects against data loss**: Resolves filename collisions automatically (e.g. `report.pdf` ➔ `report_1.pdf`) so no file is ever overwritten.
5. **Provides a Dry-Run Mode**: Allows users to preview moves safely before executing.

---

## 📂 Project Structure

```text
file-organizer/
├── .gitignore                    # Standard Python gitignore (__pycache__, IDE configs, OS files)
├── README.md                     # Documentation, usage guide, and interview answers
├── before_after_structure.txt    # Generated tree diagram capturing before/after states
├── create_test_files.py          # Sandbox dummy file generator (~20 mixed files + duplicate collision tests)
├── file_organizer.py             # Main CLI organizer script (pathlib + shutil)
└── test_directory/               # Safe sandbox folder for testing
    ├── Documents/                # (Pre-existing baseline file for collision testing)
    ├── Images/                   # (Pre-existing baseline file for collision testing)
    └── ... (23 loose dummy files across all categories)
```

---

## 🏷️ Category Mappings

| Category | File Extensions Handled |
| :--- | :--- |
| **Images** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg` |
| **Documents** | `.pdf`, `.doc`, `.docx`, `.txt`, `.pptx`, `.xlsx`, `.csv` |
| **Videos** | `.mp4`, `.mkv`, `.avi`, `.mov` |
| **Audio** | `.mp3`, `.wav`, `.aac` |
| **Archives** | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.tar.gz` |
| **Code** | `.py`, `.js`, `.html`, `.css`, `.java`, `.cpp` |
| **Others** | Unrecognized extensions (e.g., `.bin`, `.xyz`) and extensionless files |

---

## 🚀 How to Run

### 1. Requirements
- Python 3.8 or newer (tested with Python 3.14).
- Standard library only (`pathlib`, `shutil`, `argparse`). No third-party pip packages required!

### 2. Generate Safe Sandbox Files
To test without endangering any personal files, generate a sandbox directory populated with 23 diverse files and collision targets:

```bash
python create_test_files.py
```

### 3. Run in Simulation Mode (`--dry-run`)
Simulate the organization process without altering any files on disk:

```bash
python file_organizer.py --dry-run
```
*(Defaults to `test_directory` if no path is passed)*

### 4. Execute the File Organization
Run the live organizer on the default test directory:

```bash
python file_organizer.py
```

### 5. Organize Any Custom Folder
Pass any custom folder path as an argument:

```bash
# Relative path
python file_organizer.py path/to/my_folder

# Absolute path (Windows)
python file_organizer.py "C:\Users\Username\Downloads"

# Dry run on custom path
python file_organizer.py "C:\Users\Username\Downloads" --dry-run
```

---

## 🛡️ Safe Duplicate & Collision Handling

When moving a file to a category folder, a file with the same name might already exist in the destination.
- **Unsafe behavior (default in naive scripts):** Overwriting the existing file, permanently destroying data.
- **Safe behavior (in `file_organizer.py`):** The script checks if the destination file exists (or is reserved in the current batch). If a collision occurs, it increments a counter and appends `_1`, `_2`, etc. to the stem before the extension:
  - `meeting_notes.txt` ➔ `Documents/meeting_notes_1.txt`
  - `avatar.png` ➔ `Images/avatar_1.png`
  - `backup.tar.gz` ➔ `Archives/backup_1.tar.gz` (handles compound suffixes properly)

---

## 💻 Example Terminal Output

### Dry-Run Simulation:
```text
$ python file_organizer.py --dry-run

[DRY-RUN] Starting file organization in: C:\Users\HEMA\...\file-organizer\test_directory
-----------------------------------------------------------------
[DRY-RUN] Would move: 'annual_report.pdf' -> 'Documents/annual_report.pdf'
[DRY-RUN] Would move: 'architecture_diagram.svg' -> 'Images/architecture_diagram.svg'
[DRY-RUN] Would move: 'avatar.png' -> 'Images/avatar_1.png' (renamed from 'avatar.png')
[DRY-RUN] Would move: 'company_logo.png' -> 'Images/company_logo.png'
[DRY-RUN] Would move: 'customer_records.csv' -> 'Documents/customer_records.csv'
[DRY-RUN] Would move: 'data_pipeline.py' -> 'Code/data_pipeline.py'
[DRY-RUN] Would move: 'dataset_weights.bin' -> 'Others/dataset_weights.bin'
[DRY-RUN] Would move: 'financial_budget.xlsx' -> 'Documents/financial_budget.xlsx'
[DRY-RUN] Would move: 'frontend_app.js' -> 'Code/frontend_app.js'
[DRY-RUN] Would move: 'index.html' -> 'Code/index.html'
[DRY-RUN] Would move: 'loading_spinner.gif' -> 'Images/loading_spinner.gif'
[DRY-RUN] Would move: 'meeting_notes.txt' -> 'Documents/meeting_notes_1.txt' (renamed from 'meeting_notes.txt')
[DRY-RUN] Would move: 'notification_chime.wav' -> 'Audio/notification_chime.wav'
[DRY-RUN] Would move: 'podcast_ep22.mp3' -> 'Audio/podcast_ep22.mp3'
[DRY-RUN] Would move: 'product_demo.mp4' -> 'Videos/product_demo.mp4'
[DRY-RUN] Would move: 'project_proposal.docx' -> 'Documents/project_proposal.docx'
[DRY-RUN] Would move: 'quarterly_presentation.pptx' -> 'Documents/quarterly_presentation.pptx'
[DRY-RUN] Would move: 'RELEASE_NOTES' -> 'Others/RELEASE_NOTES'
[DRY-RUN] Would move: 'screen_recording.mkv' -> 'Videos/screen_recording.mkv'
[DRY-RUN] Would move: 'server_logs.tar.gz' -> 'Archives/server_logs.tar.gz'
[DRY-RUN] Would move: 'system_backup.zip' -> 'Archives/system_backup.zip'
[DRY-RUN] Would move: 'theme_styles.css' -> 'Code/theme_styles.css'
[DRY-RUN] Would move: 'vacation_photo.jpg' -> 'Images/vacation_photo.jpg'

==================================================
         DRY-RUN SUMMARY (NO FILES MOVED)         
==================================================
Category                               Files Moved
--------------------------------------------------
Archives                                         2
Audio                                            2
Code                                             4
Documents                                        6
Images                                           5
Others                                           2
Videos                                           2
--------------------------------------------------
Total                                           23
==================================================
```

### Live Organization Run:
```text
$ python file_organizer.py

Starting file organization in: C:\Users\HEMA\...\file-organizer\test_directory
-----------------------------------------------------------------
Moved: 'annual_report.pdf' -> 'Documents/annual_report.pdf'
Moved: 'architecture_diagram.svg' -> 'Images/architecture_diagram.svg'
Moved: 'avatar.png' -> 'Images/avatar_1.png' (renamed from 'avatar.png')
Moved: 'company_logo.png' -> 'Images/company_logo.png'
Moved: 'customer_records.csv' -> 'Documents/customer_records.csv'
Moved: 'data_pipeline.py' -> 'Code/data_pipeline.py'
Moved: 'dataset_weights.bin' -> 'Others/dataset_weights.bin'
Moved: 'financial_budget.xlsx' -> 'Documents/financial_budget.xlsx'
Moved: 'frontend_app.js' -> 'Code/frontend_app.js'
Moved: 'index.html' -> 'Code/index.html'
Moved: 'loading_spinner.gif' -> 'Images/loading_spinner.gif'
Moved: 'meeting_notes.txt' -> 'Documents/meeting_notes_1.txt' (renamed from 'meeting_notes.txt')
Moved: 'notification_chime.wav' -> 'Audio/notification_chime.wav'
Moved: 'podcast_ep22.mp3' -> 'Audio/podcast_ep22.mp3'
Moved: 'product_demo.mp4' -> 'Videos/product_demo.mp4'
Moved: 'project_proposal.docx' -> 'Documents/project_proposal.docx'
Moved: 'quarterly_presentation.pptx' -> 'Documents/quarterly_presentation.pptx'
Moved: 'RELEASE_NOTES' -> 'Others/RELEASE_NOTES'
Moved: 'screen_recording.mkv' -> 'Videos/screen_recording.mkv'
Moved: 'server_logs.tar.gz' -> 'Archives/server_logs.tar.gz'
Moved: 'system_backup.zip' -> 'Archives/system_backup.zip'
Moved: 'theme_styles.css' -> 'Code/theme_styles.css'
Moved: 'vacation_photo.jpg' -> 'Images/vacation_photo.jpg'

==================================================
               ORGANIZATION SUMMARY               
==================================================
Category                               Files Moved
--------------------------------------------------
Archives                                         2
Audio                                            2
Code                                             4
Documents                                        6
Images                                           5
Others                                           2
Videos                                           2
--------------------------------------------------
Total                                           23
==================================================
```

---

## 🌳 Before vs After Tree Structure

See [before_after_structure.txt](before_after_structure.txt) for the complete generated tree. Here is an excerpt:

```text
BEFORE ORGANIZATION                        AFTER ORGANIZATION
test_directory/                            test_directory/
├── Documents/                             ├── Archives/
│   └── meeting_notes.txt                  │   ├── server_logs.tar.gz
├── Images/                                │   └── system_backup.zip
│   └── avatar.png                         ├── Audio/
├── annual_report.pdf                      │   ├── notification_chime.wav
├── architecture_diagram.svg               │   └── podcast_ep22.mp3
├── avatar.png                             ├── Code/
├── customer_records.csv                   │   ├── data_pipeline.py
├── data_pipeline.py                       │   ├── frontend_app.js
├── dataset_weights.bin                    │   ├── index.html
├── financial_budget.xlsx                  │   └── theme_styles.css
├── frontend_app.js                        ├── Documents/
├── index.html                             │   ├── annual_report.pdf
├── loading_spinner.gif                    │   ├── customer_records.csv
├── meeting_notes.txt                      │   ├── financial_budget.xlsx
├── notification_chime.wav                 │   ├── meeting_notes.txt
├── podcast_ep22.mp3                       │   ├── meeting_notes_1.txt   <-- Renamed safely
├── product_demo.mp4                       │   ├── project_proposal.docx
├── project_proposal.docx                  │   └── quarterly_presentation.pptx
├── quarterly_presentation.pptx            ├── Images/
├── RELEASE_NOTES                          │   ├── architecture_diagram.svg
├── screen_recording.mkv                   │   ├── avatar.png
├── server_logs.tar.gz                     │   ├── avatar_1.png          <-- Renamed safely
├── system_backup.zip                      │   ├── company_logo.png
├── theme_styles.css                       │   ├── loading_spinner.gif
└── vacation_photo.jpg                     │   └── vacation_photo.jpg
                                           ├── Others/
                                           │   ├── dataset_weights.bin
                                           │   └── RELEASE_NOTES
                                           └── Videos/
                                               ├── product_demo.mp4
                                               └── screen_recording.mkv
```

---

## 🎓 Technical Interview Questions & Answers

### 1. What is `pathlib`?
`pathlib` is an object-oriented filesystem path library introduced in Python 3.4. Instead of treating file paths as fragile raw strings that require manual string concatenation or `os.path.join()`, `pathlib.Path` represents paths as rich objects with convenient methods and properties:
- **Intuitive Path Construction:** Uses the division operator `/` (e.g. `base_dir / "Documents" / "file.txt"`), which automatically formats the correct directory separator (`/` on Linux/macOS, `\` on Windows).
- **Built-in Inspection Properties:** Offers readable properties like `.name`, `.stem`, `.suffix`, `.parent`, `.is_file()`, and `.is_dir()`.
- **Integrated Operations:** Methods like `.mkdir(parents=True, exist_ok=True)`, `.iterdir()`, and `.glob()` eliminate boilerplate code.

### 2. What is the difference between `os` and `shutil`?
Both modules are part of Python's standard library, but they operate at different levels of abstraction:
- **`os` (Operating System Interface):** Provides low-level operating system interactions and single-item operations (e.g., `os.remove()`, `os.rename()`, `os.mkdir()`, environment variables, and process IDs). It does not provide high-level composite functions like recursively copying or moving trees.
- **`shutil` (Shell Utilities):** Provides high-level composite file operations modeled after Unix shell commands. It specializes in actions like recursively copying directories (`shutil.copytree()`), recursively deleting directories (`shutil.rmtree()`), moving files across different drives or partitions (`shutil.move()`), and inspecting disk usage (`shutil.disk_usage()`).
- *Summary:* Use `os` for low-level OS calls and permissions; use `shutil` for moving, copying, and archiving whole files and folder hierarchies.

### 3. How can Python automate repetitive file-management tasks?
Python provides an unmatched ecosystem for file automation due to:
1. **Batteries-Included Standard Library:** Modules like `pathlib`, `shutil`, `glob`, `fnmatch`, `hashlib`, and `zipfile` enable searching, filtering, renaming, hashing, and compression without installing third-party packages.
2. **Scheduled and Event-Driven Triggers:** Python scripts can be scheduled via OS cron jobs (Linux/macOS) or Windows Task Scheduler, or triggered in real time upon file arrival using file-watching libraries like `watchdog`.
3. **Cross-Platform Compatibility:** Python abstracts away differences in path separators, file permissions, and newline characters across Windows, Linux, and macOS.
4. **Data Integrity:** Scripts can calculate checksums (`hashlib.md5`/`sha256`) before and after operations, simulate dry runs, log actions, and implement rollback mechanisms.

---

## 🐙 Git Commands to Push to GitHub

To push this project to a new repository named `file-organizer` on your GitHub account, run these commands in your terminal:

```bash
# 1. Navigate to the project directory
cd "C:\Users\HEMA\.gemini\antigravity\scratch\file-organizer"

# 2. Initialize a local git repository
git init

# 3. Add all project files (respecting .gitignore)
git add .

# 4. Commit the initial build
git commit -m "feat: complete Task 22 File Organizer with safe collision handling, dry-run, and tests"

# 5. Rename the default branch to main
git branch -M main

# 6. Link your local repository to your remote GitHub repository
# (Replace YOUR_GITHUB_USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/file-organizer.git

# 7. Push your code to GitHub
git push -u origin main
```
