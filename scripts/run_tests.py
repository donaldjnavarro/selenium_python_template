# run_tests.py
from __future__ import annotations

import os
import subprocess
import sys
import shutil
import datetime

from dotenv import load_dotenv


def set_runtime_env_vars():
    """Set up and standardize environment variables for test reports."""
    # Standardize the name and location of the report directories
    REPORT_DIR = "reports"

    # Main report directory for the "latest" run
    if "LATEST_REPORT_DIR" not in os.environ:
        LATEST_REPORT_DIR = f"{REPORT_DIR}/latest"
        os.environ["LATEST_REPORT_DIR"] = LATEST_REPORT_DIR
        os.makedirs(LATEST_REPORT_DIR, exist_ok=True)

    if "LATEST_SCREENSHOT_DIR" not in os.environ:
        LATEST_SCREENSHOT_DIR = f"{REPORT_DIR}/latest/screenshots"
        os.environ["LATEST_SCREENSHOT_DIR"] = LATEST_SCREENSHOT_DIR
        os.makedirs(LATEST_SCREENSHOT_DIR, exist_ok=True)

    # Timestamped report directory for historical runs

    if "RUN_TIMESTAMP" not in os.environ:
        # Store a timestamp to represent the current run
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.environ["RUN_TIMESTAMP"] = timestamp

    if "TIMESTAMPED_REPORT_DIR" not in os.environ:
        TIMESTAMPED_REPORT_DIR = f"{REPORT_DIR}/{timestamp}"
        os.environ["TIMESTAMPED_REPORT_DIR"] = TIMESTAMPED_REPORT_DIR
        os.makedirs(TIMESTAMPED_REPORT_DIR, exist_ok=True)

    if "TIMESTAMPED_SCREENSHOT_DIR" not in os.environ:
        TIMESTAMPED_SCREENSHOT_DIR = f"{REPORT_DIR}/{timestamp}/screenshots"
        os.environ["TIMESTAMPED_SCREENSHOT_DIR"] = TIMESTAMPED_SCREENSHOT_DIR
        os.makedirs(TIMESTAMPED_SCREENSHOT_DIR, exist_ok=True)


def update_report_flag(args, required_flags="F"):
    """Ensure the -r flag includes all required summary characters.

    Mutates args in place if needed.
    """
    for i, arg in enumerate(args):
        if arg.startswith("-r"):
            existing_flags = arg[2:]
            missing_flags = ''.join(
                c for c in required_flags if c not in existing_flags
            )
            if missing_flags:
                args[i] = f"-r{existing_flags}{missing_flags}"
            return
    # No -r flag found
    args.insert(1, f"-r{required_flags}")


def main():
    """Handle all customization for running tests with a single command"""
    set_runtime_env_vars()
    load_dotenv()

    args = sys.argv[1:]  # User-supplied args
    final_args = ["pytest"] + args

    # Handle parallel flag
    if os.getenv("PARALLEL", "false").lower() == "true":
        if not any(arg.startswith("-n") for arg in args):
            final_args.insert(1, "auto")
            final_args.insert(1, "-n")
        print(
            "[\033[93mWARNING\033[0m] "
            "Parallelization may cause logs to be suppressed."
        )

    # Handle quiet flag
    if os.getenv("QUIET", "false").lower() == "true":
        if "-q" not in args and "--quiet" not in args:
            final_args.insert(1, "-q")
        if not any(arg.startswith("--tb") for arg in args):
            final_args.insert(1, "--tb=short")
        update_report_flag(final_args, required_flags="F")

    # Default to skipping certain test groups if no markers are specified
    if not any(arg.startswith("-m") for arg in args):
        final_args += ["-m", "not skip"]

    # Display logs
    final_args += ["--disable-warnings", "-s"]

    # Generate HTML report

    latest_report = (
        f"{os.getenv('LATEST_REPORT_DIR', 'reports/latest')}"
        "/test_report.html"
    )

    if not any(arg.startswith("--html") for arg in args):
        final_args += [
            f"--html={latest_report}",
            "--self-contained-html",
        ]

    # Run the full test command
    print(f"Running test command: {' '.join(final_args)}")
    subprocess.run(final_args)

    # Copy the report into an archive with a timestamp
    if os.getenv("SAVE_HISTORICAL_REPORTS", "false").lower() == "true":
        archive_report = (
            f"{os.getenv(
                'TIMESTAMPED_REPORT_DIR',
                'reports/unknown_timestamp'
            )}"
            f"/test_report.html"
        )
        shutil.copyfile(latest_report, archive_report)

if __name__ == "__main__":
    main()
