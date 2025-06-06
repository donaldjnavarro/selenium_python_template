# run_tests.py
from __future__ import annotations

import os
import subprocess
import sys
import shutil
import datetime
from pathlib import Path

from dotenv import load_dotenv
from logging import getLogger

logger = getLogger(__name__)

def set_runtime_env_vars():
    """Set up and standardize environment variables for test reports."""
    # Standardize the name and location of the report directories
    REPORT_FOLDER = "reports"
    LATEST_FOLDER = "latest"
    SCREENSHOT_FOLDER = "screenshots"

    # Timestamped report directory for historical runs
    # Store a timestamp to represent the current run
    if "RUN_TIMESTAMP" not in os.environ:
        os.environ["RUN_TIMESTAMP"] = (
            datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        )

    # Create main report folders
    for name, path in {
        "LATEST_REPORT_DIR": (
            Path(REPORT_FOLDER) /
            LATEST_FOLDER
        ),
        "LATEST_SCREENSHOT_DIR": (
            Path(REPORT_FOLDER) /
            LATEST_FOLDER /
            SCREENSHOT_FOLDER
        )
    }.items():
        if name not in os.environ:
            os.environ[name] = str(path)

    # Create archive folders
    if os.getenv("SAVE_HISTORICAL_REPORTS", "false").lower() == "true":
        for name, path in {
            "TIMESTAMPED_REPORT_DIR": (
                Path(REPORT_FOLDER) /
                os.environ['RUN_TIMESTAMP']
            ),
            "TIMESTAMPED_SCREENSHOT_DIR": (
                Path(REPORT_FOLDER) /
                os.environ['RUN_TIMESTAMP'] /
                SCREENSHOT_FOLDER
            )
        }.items():
            if name not in os.environ:
                os.environ[name] = str(path)
                os.makedirs(path, exist_ok=True)

def create_folders():
    """Create and manage report and screenshot directories for test runs."""
    # Delete the previous "latest" report folder if it exists
    latest_report_dir = Path(os.environ['LATEST_REPORT_DIR'])

    if latest_report_dir.exists() and latest_report_dir.is_dir():
        shutil.rmtree(latest_report_dir)

    # Create fresh directory for the new latest report
    os.makedirs(
        latest_report_dir,
        exist_ok=True
    )
    os.makedirs(
        Path(os.environ['LATEST_SCREENSHOT_DIR']),
        exist_ok=True
    )

    # Create the archive directory if .env is configured for it
    if os.getenv("SAVE_HISTORICAL_REPORTS", "false").lower() == "true":
        os.makedirs(
            Path(os.environ['TIMESTAMPED_REPORT_DIR']),
            exist_ok=True
        )
        os.makedirs(
            Path(os.environ['TIMESTAMPED_SCREENSHOT_DIR']),
            exist_ok=True
        )
class PytestCommandBuilder:
    """Builds and manages the pytest command arguments for running tests."""

    def __init__(self, user_args: list[str]):
        """Initialize the PytestCommandBuilder with user-provided arguments.

        Initialization Steps:
            - Sets up the base pytest command.
            - Determines the report output directory
            - Applies various configuration methods to:
                - Update the report flag for pytest.
                - Enable or disable quiet mode.
                - Skip tests marked with specific markers.
                - Configure test parallelization.
                - Enable HTML reporting.
                - Adjust console display settings for test output.

        This constructor ensures that all necessary test runner 
        configurations are applied before executing tests.

        Args:
            user_args (list[str]): A list of command-line arguments

        Attributes:
            _args (list[str]): Stores the user-provided arguments.
            command (list[str]): The base command to invoke pytest.
            report_path (str): The file path for the HTML test report.

        """
        self._args = user_args

        # Static data
        self.command = ["pytest"]
        self.report_path = str(
            Path(
                os.getenv("LATEST_REPORT_DIR", "reports/latest")
            ) / "test_report.html"
        )

        # Apply class logic
        self._update_report_flag()
        self._quiet()
        self._skip_marked_tests()
        self._parallelization()
        self._html_reporting()
        self._configure_console_display()

    def _update_report_flag(self, required_flags="F"):
        """Ensure the -r flag includes all required summary characters."""
        for i, arg in enumerate(self._args):
            if arg.startswith("-r"):
                existing_flags = arg[2:]
                missing_flags = ''.join(
                    c for c in required_flags if c not in existing_flags
                )
                if missing_flags:
                    self._args[i] = f"-r{existing_flags}{missing_flags}"
                return

        # Safe place to insert -r flag without breaking -m and its expression
        insert_pos = len(self._args)
        i = 0
        while i < len(self._args):
            if self._args[i] == "-m" and i + 1 < len(self._args):
                i += 2  # Skip marker and its expression
            else:
                insert_pos = i + 1
                i += 1

        self._args.insert(insert_pos, f"-r{required_flags}")


    def _quiet(self):
        """Collect flags to reduce console output verbosity.

        Only applies if the QUIET environment variable is set to true.
        """
        if os.getenv("QUIET", "false").lower() == "true":
            if "-q" not in self._args and "--quiet" not in self._args:
                self._args.insert(0, "-q")
            if not any(arg.startswith("--tb") for arg in self._args):
                self._args.insert(0, "--tb=short")
            self._update_report_flag(required_flags="F")

    def _skip_marked_tests(self):
        """Ensure the default marker expression includes 'not skip'."""
        new_args = []
        user_marker_expr_parts = []
        i = 0

        while i < len(self._args):
            arg = self._args[i]
            if arg == "-m":
                i += 1
                # Collect everything until the next flag (starts with -)
                while (
                    i < len(self._args)
                    and not self._args[i].startswith("-")
                ):
                    user_marker_expr_parts.append(self._args[i])
                    i += 1
            else:
                new_args.append(arg)
                i += 1

        # Build the final marker expression
        if user_marker_expr_parts:
            user_expr = " ".join(user_marker_expr_parts)
            combined_expr = f"not skip and ({user_expr})"
        else:
            combined_expr = "not skip"

        new_args += ["-m", combined_expr]
        self._args = new_args

    def _parallelization(self):
        """Add flags to enable parallel test execution if requested.

        Only applies if the PARALLEL environment variable is set to true.
        """
        # Handle parallel flag
        if os.getenv("PARALLEL", "false").lower() == "true":
            if not any(arg.startswith("-n") for arg in self._args):
                self._args.insert(1, "auto")
                self._args.insert(1, "-n")
            print(
                "[\033[93mWARNING\033[0m] "
                "Parallelization may cause logs to be suppressed."
            )

    def _html_reporting(self):
        """Add reporting-related flags to the pytest command arguments."""
        if not any(arg.startswith("--html") for arg in self._args):
            # HTML report pytest arguments
            self._args += [
                f"--html={self.report_path}",
                "--self-contained-html"
            ]
    
    def _configure_console_display(self):
        """Add any user-supplied arguments to the final command."""
        if "--disable-warnings" not in self._args:
            self._args.append("--disable-warnings")
        if "-s" not in self._args:
            self._args.append("-s")

    @property
    def full_command(self) -> list[str]:
        """Get the full pytest command with all arguments.
        
        Collects all the flags configured by this class's methods.
        """
        return self.command + self._args

def historical_report(current_report_path: str | None = None):
    """Copy the current test report to a timestamped archive.

    Only acts if toggled on in .env
    """
    if os.getenv("SAVE_HISTORICAL_REPORTS", "false").lower() == "true":
        archive_report = (
            f"{os.getenv(
                'TIMESTAMPED_REPORT_DIR',
                'reports/unknown_timestamp'
            )}"
            f"/test_report.html"
        )
        os.makedirs(os.path.dirname(archive_report), exist_ok=True)
        if os.path.exists(current_report_path):
            shutil.copyfile(current_report_path, archive_report)
        else:
            print("[WARNING] No test report found to archive.")

def main():
    """Handle all customization for running tests with a single command"""
    # Set up environment variables
    load_dotenv()
    set_runtime_env_vars()
    create_folders()

    # Prepare pytest command for the console
    user_args = sys.argv[1:]
    pytest_command_builder = PytestCommandBuilder(user_args)
    cmd = pytest_command_builder.full_command

    # Run the full pytest command
    print(f"Running test command: {' '.join(
        cmd
    )}")
    print(f"Test run started at {os.environ['RUN_TIMESTAMP']}")
    subprocess.run(cmd)

    # Copy the test report into an archive with a timestamp
    historical_report(pytest_command_builder.report_path)

if __name__ == "__main__":
    main()
