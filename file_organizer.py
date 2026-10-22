"""
file_organizer.py
-----------------
A Python utility that automatically scans a target directory and organizes
loose files into categorized subfolders based on file extensions.

Features:
- Pathlib-based file system traversal and manipulation.
- Shutil-based file moving.
- Automatic extension-to-category mapping (Images, Documents, Videos, Audio, Archives, Code, Others).
- Safe duplicate filename handling (renames incoming files with _1, _2 suffixes instead of overwriting).
- Category folder creation on demand (only creates folders when needed).
- Skips existing subdirectories and the script itself.
- Dry-run simulation mode (--dry-run).
- Formatted summary report of organized files.
- Robust error handling for missing directories and permission issues.
"""

import argparse
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Mapping of category folder names to sets of recognized file extensions.
# All extensions are stored in lowercase for case-insensitive matching.
CATEGORY_MAPPINGS: Dict[str, Set[str]] = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".pptx", ".xlsx", ".csv"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov"},
    "Audio": {".mp3", ".wav", ".aac"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".tar.gz"},
    "Code": {".py", ".js", ".html", ".css", ".java", ".cpp"},
}

DEFAULT_CATEGORY = "Others"


def determine_category(file_path: Path) -> str:
    """
    Determine the category folder for a given file path based on its extension.

    Args:
        file_path (Path): Path object representing the file.

    Returns:
        str: Category name (e.g., 'Documents', 'Images', or 'Others').
    """
    filename_lower = file_path.name.lower()

    # Special check for compound archive extensions like .tar.gz
    if filename_lower.endswith(".tar.gz"):
        return "Archives"

    # Standard extension check using pathlib.Path.suffix
    extension = file_path.suffix.lower()

    if not extension:
        # Files without extensions (e.g. 'LICENSE', 'Dockerfile') go to Others
        return DEFAULT_CATEGORY

    for category, extensions in CATEGORY_MAPPINGS.items():
        if extension in extensions:
            return category

    return DEFAULT_CATEGORY


def get_unique_destination(
    destination_folder: Path,
    original_filename: str,
    reserved_destinations: Set[Path],
) -> Tuple[Path, bool]:
    """
    Calculate a collision-free destination Path within destination_folder.
    If a file with the same name already exists on disk or was planned in the
    current execution batch, appends '_1', '_2', etc., before the file extension.

    Args:
        destination_folder (Path): The category folder where the file will be placed.
        original_filename (str): The original name of the file (e.g., 'report.pdf').
        reserved_destinations (Set[Path]): Set of paths already assigned in this batch
                                          (ensures uniqueness even during dry-run).

    Returns:
        Tuple[Path, bool]: (unique_destination_path, was_renamed)
    """
    destination_path = destination_folder / original_filename

    # If the file doesn't exist and hasn't been reserved, return as is
    if not destination_path.exists() and destination_path not in reserved_destinations:
        return destination_path, False

    # Handle compound extensions like .tar.gz separately from single extensions
    lower_name = original_filename.lower()
    if lower_name.endswith(".tar.gz"):
        stem = original_filename[:-7]
        extension = original_filename[-7:]
    else:
        file_obj = Path(original_filename)
        stem = file_obj.stem
        extension = file_obj.suffix

    counter = 1
    while destination_path.exists() or destination_path in reserved_destinations:
        new_filename = f"{stem}_{counter}{extension}"
        destination_path = destination_folder / new_filename
        counter += 1

    return destination_path, True


def organize_directory(target_path: Path, dry_run: bool = False) -> Dict[str, int]:
    """
    Scan the target directory and organize loose files into category folders.

    Args:
        target_path (Path): Path to the directory to organize.
        dry_run (bool): If True, simulate actions without modifying the filesystem.

    Returns:
        Dict[str, int]: Dictionary mapping category names to number of files moved.
    """
    # Validate target directory existence
    if not target_path.exists():
        print(f"[ERROR] Target path does not exist: '{target_path}'", file=sys.stderr)
        sys.exit(1)

    if not target_path.is_dir():
        print(f"[ERROR] Target path is a file, not a directory: '{target_path}'", file=sys.stderr)
        sys.exit(1)

    # Resolve absolute paths to safely skip the organizer script itself
    current_script_path = Path(__file__).resolve()

    # Track files moved per category
    category_counts: Dict[str, int] = defaultdict(int)
    reserved_destinations: Set[Path] = set()

    # Collect only direct files (skip subfolders and this script)
    try:
        entries = list(target_path.iterdir())
    except PermissionError as err:
        print(f"[ERROR] Permission denied reading target directory: {err}", file=sys.stderr)
        sys.exit(1)

    files_to_process: List[Path] = []
    for item in entries:
        # Skip directories - only organize loose files in target directory root
        if not item.is_file():
            continue

        # Skip the organizer script itself if it happens to be in target_path
        if item.resolve() == current_script_path:
            continue

        files_to_process.append(item)

    if not files_to_process:
        print(f"[INFO] No loose files found to organize in '{target_path}'.")
        return dict(category_counts)

    mode_prefix = "[DRY-RUN] " if dry_run else ""
    print(f"\n{mode_prefix}Starting file organization in: {target_path.resolve()}")
    print("-" * 65)

    for file_path in sorted(files_to_process, key=lambda p: p.name.lower()):
        category = determine_category(file_path)
        dest_folder = target_path / category

        dest_file_path, was_renamed = get_unique_destination(
            dest_folder, file_path.name, reserved_destinations
        )
        reserved_destinations.add(dest_file_path)

        # Logging output for user visibility
        rename_note = f" (renamed from '{file_path.name}')" if was_renamed else ""
        action_desc = "Would move" if dry_run else "Moved"
        print(
            f"{mode_prefix}{action_desc}: '{file_path.name}' -> '{category}/{dest_file_path.name}'{rename_note}"
        )

        if not dry_run:
            try:
                # Create category folder only when needed (exist_ok prevents errors)
                dest_folder.mkdir(parents=True, exist_ok=True)

                # Safely move the file
                shutil.move(str(file_path), str(dest_file_path))
                category_counts[category] += 1
            except PermissionError as err:
                print(f"[ERROR] Permission denied while moving '{file_path.name}': {err}", file=sys.stderr)
            except OSError as err:
                print(f"[ERROR] Operating system error moving '{file_path.name}': {err}", file=sys.stderr)
        else:
            # In dry-run, count as simulated move
            category_counts[category] += 1

    return dict(category_counts)


def print_summary(category_counts: Dict[str, int], dry_run: bool = False) -> None:
    """
    Print a formatted summary table of the organization operation.

    Args:
        category_counts (Dict[str, int]): Number of files moved per category.
        dry_run (bool): Whether the execution was a simulation.
    """
    mode_header = "DRY-RUN SUMMARY (NO FILES MOVED)" if dry_run else "ORGANIZATION SUMMARY"
    print("\n" + "=" * 50)
    print(f"{mode_header:^50}")
    print("=" * 50)
    print(f"{'Category':<30}{'Files Moved':>20}")
    print("-" * 50)

    if not category_counts:
        print(f"{'No files processed':<30}{'0':>20}")
    else:
        total_files = 0
        for category in sorted(category_counts.keys()):
            count = category_counts[category]
            total_files += count
            print(f"{category:<30}{count:>20}")
        print("-" * 50)
        print(f"{'Total':<30}{total_files:>20}")

    print("=" * 50 + "\n")


def parse_arguments() -> argparse.Namespace:
    """
    Configure and parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments with target and dry_run flags.
    """
    parser = argparse.ArgumentParser(
        description="Organize loose files in a folder into category subfolders based on extensions.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python file_organizer.py\n"
            "  python file_organizer.py test_directory\n"
            "  python file_organizer.py C:/Users/Name/Downloads --dry-run\n"
        ),
    )

    parser.add_argument(
        "target",
        nargs="?",
        default="test_directory",
        help="Path to the target directory to organize (default: 'test_directory')",
    )

    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Simulate the organization process without actually moving or renaming any files.",
    )

    return parser.parse_args()


def main() -> None:
    """
    Main entry point for the script.
    """
    args = parse_arguments()
    target_path = Path(args.target)

    counts = organize_directory(target_path=target_path, dry_run=args.dry_run)
    print_summary(counts, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
