import argparse
import sys
from pathlib import Path

from duplicate_detector.scanner import scan_directory
from duplicate_detector.detector import find_duplicates
from duplicate_detector.reporter import (
    create_report,
    print_report,
    save_json_report
)


def main():
    parser = argparse.ArgumentParser(
        description="Find duplicate files in a directory."
    )

    parser.add_argument(
        "--path",
        required=True,
        help="Directory to scan"
    )

    parser.add_argument(
        "--output",
        help="Optional JSON report output file"
    )

    args = parser.parse_args()

    directory = Path(args.path)

    if not directory.exists():
        print(f"Error: Path does not exist: {args.path}")
        sys.exit(1)

    if not directory.is_dir():
        print(f"Error: Path is not a directory: {args.path}")
        sys.exit(1)

    print(f"Scanning directory: {args.path}")

    files = scan_directory(args.path)

    print(f"Files found: {len(files)}")

    duplicate_groups = find_duplicates(files)

    report = create_report(
        total_files_scanned=len(files),
        duplicate_groups=duplicate_groups
    )

    print_report(report)

    if args.output:
        save_json_report(report, args.output)
        print(f"\nReport saved to: {args.output}")


if __name__ == "__main__":
    main()