# run_tests.py
import os
import sys
import subprocess
from dotenv import load_dotenv


def update_report_flag(args, required_flags="F"):
    """
    Ensure the -r flag includes all required summary characters.
    Mutates args in place if needed.
    """
    for i, arg in enumerate(args):
        if arg.startswith("-r"):
            existing_flags = arg[2:]
            missing_flags = ''.join(c for c in required_flags if c not in existing_flags)
            if missing_flags:
                args[i] = f"-r{existing_flags}{missing_flags}"
            return
    # No -r flag found
    args.insert(1, f"-r{required_flags}")


def main():
    """
    Handles all customization for running tests with pytest by packing them into a single command line call.
    """
    load_dotenv()

    args = sys.argv[1:]  # User-supplied args
    final_args = ["pytest"] + args

    # Handle parallel flag
    if os.getenv("PARALLEL", "false").lower() == "true":
        if not any(arg.startswith("-n") for arg in args):
            final_args.insert(1, "auto")
            final_args.insert(1, "-n")

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

    print(f"Running test command: {' '.join(final_args)}")
    subprocess.run(final_args)


if __name__ == "__main__":
    main()
