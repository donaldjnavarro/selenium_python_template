# run_tests.py
from __future__ import annotations

import os
import subprocess
import sys

from dotenv import load_dotenv


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

    print(f"Running test command: {' '.join(final_args)}")
    subprocess.run(final_args)


if __name__ == "__main__":
    main()
