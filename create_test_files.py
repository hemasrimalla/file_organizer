"""
create_test_files.py
--------------------
Utility script to generate a safe sandbox folder ('test_directory') populated
with ~20 dummy files across diverse categories and extensions.

To safely test duplicate filename resolution:
Pre-creates duplicate files in destination subfolders (e.g. Documents/meeting_notes.txt),
allowing the organizer script to prove that it safely renames incoming files
(e.g. to meeting_notes_1.txt) rather than overwriting them.
"""

import argparse
import shutil
from pathlib import Path

# Sample files to create directly inside test_directory root
SAMPLE_FILES = [
    # Images (.jpg, .jpeg, .png, .gif, .bmp, .svg)
    ("vacation_photo.jpg", "Binary photo content [JPEG sample]"),
    ("company_logo.png", "Binary PNG image data for logo"),
    ("avatar.png", "New avatar image uploaded by user"),  # Duplicate target!
    ("loading_spinner.gif", "Animated GIF data"),
    ("architecture_diagram.svg", "<svg><circle cx='50' cy='50' r='40'/></svg>"),

    # Documents (.pdf, .doc, .docx, .txt, .pptx, .xlsx, .csv)
    ("annual_report.pdf", "%PDF-1.4 dummy annual report content"),
    ("meeting_notes.txt", "New meeting notes taken today on project roadmap"),  # Duplicate target!
    ("project_proposal.docx", "Word document dummy XML structure"),
    ("quarterly_presentation.pptx", "PowerPoint presentation slides data"),
    ("financial_budget.xlsx", "Excel spreadsheet data - Q1 to Q4 budget"),
    ("customer_records.csv", "id,name,email\n1,Alice,alice@example.com\n2,Bob,bob@example.com"),

    # Videos (.mp4, .mkv, .avi, .mov)
    ("product_demo.mp4", "MP4 video stream payload"),
    ("screen_recording.mkv", "MKV video file container sample"),

    # Audio (.mp3, .wav, .aac)
    ("podcast_ep22.mp3", "ID3 audio frame content"),
    ("notification_chime.wav", "RIFF WAVE sound sample"),

    # Archives (.zip, .rar, .7z, .tar, .gz, .tar.gz)
    ("system_backup.zip", "PK zip archive container"),
    ("server_logs.tar.gz", "Gzip compressed tarball archive"),

    # Code (.py, .js, .html, .css, .java, .cpp)
    ("data_pipeline.py", "print('Pipeline running successfully!')\n"),
    ("frontend_app.js", "console.log('App initialized');\n"),
    ("index.html", "<!DOCTYPE html><html><body><h1>Hello World</h1></body></html>"),
    ("theme_styles.css", "body { margin: 0; background-color: #f4f4f4; }"),

    # Others (unrecognized extensions and files without extension)
    ("dataset_weights.bin", "Raw binary weight tensor buffer"),
    ("RELEASE_NOTES", "Release notes for version 1.0 (no file extension)"),
]

# Pre-existing files placed inside subfolders to verify collision resolution
PRE_EXISTING_SUBFOLDER_FILES = [
    ("Documents/meeting_notes.txt", "Old meeting notes from last quarter already archived."),
    ("Images/avatar.png", "Old avatar graphic already present in Images."),
]


def create_test_environment(target_dir: Path, clean: bool = True) -> None:
    """
    Populate target_dir with sample dummy files and pre-existing collision files.

    Args:
        target_dir (Path): The directory to populate.
        clean (bool): If True, removes target_dir first if it already exists.
    """
    if clean and target_dir.exists():
        print(f"[CLEAN] Removing existing '{target_dir}' directory...")
        shutil.rmtree(target_dir)

    target_dir.mkdir(parents=True, exist_ok=True)
    print(f"[SETUP] Initializing test directory at: {target_dir.resolve()}")

    # 1. Create pre-existing files in subfolders to test collision handling
    print("\n[STEP 1] Placing pre-existing files in category subfolders (to test collisions):")
    for relative_path_str, content in PRE_EXISTING_SUBFOLDER_FILES:
        file_path = target_dir / relative_path_str
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        print(f"  + Pre-existing: {relative_path_str}")

    # 2. Create loose files in the root of target_dir
    print(f"\n[STEP 2] Creating {len(SAMPLE_FILES)} loose files in '{target_dir.name}':")
    for filename, content in SAMPLE_FILES:
        file_path = target_dir / filename
        file_path.write_text(content, encoding="utf-8")
        print(f"  + Created: {filename}")

    total_created = len(SAMPLE_FILES) + len(PRE_EXISTING_SUBFOLDER_FILES)
    print(f"\n[DONE] Successfully set up {total_created} test files in '{target_dir}'.")
    print("Ready to run: python file_organizer.py --dry-run")
    print("Followed by: python file_organizer.py")


def main() -> None:
    """
    Parse arguments and run test environment generation.
    """
    parser = argparse.ArgumentParser(
        description="Generate dummy files in a test directory for file organizer practice."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default="test_directory",
        help="Directory name to create test files in (default: 'test_directory')",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not wipe target directory if it already exists.",
    )

    args = parser.parse_args()
    target_path = Path(args.target)
    create_test_environment(target_dir=target_path, clean=not args.no_clean)


if __name__ == "__main__":
    main()
