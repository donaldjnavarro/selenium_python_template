from __future__ import annotations

import os
import subprocess
import sys
from typing import List


# ANSI escape codes for colors and styles
class Colors:
    """ANSI escape codes for colors and styles used in terminal output"""

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def _print_info(message: str):
    print(f"{Colors.CYAN}{Colors.BOLD}{message}{Colors.RESET}")


def _print_warning(message: str):
    print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  {message}{Colors.RESET}")


def _print_error(message: str):
    print(f"{Colors.RED}{Colors.BOLD}❌ {message}{Colors.RESET}")


def _run_ruff(args: List[str], log_filename: str, suggest_fix: bool = False):
    os.makedirs("reports", exist_ok=True)
    report_path = os.path.join("reports", log_filename)

    _print_info(f"Running: ruff {' '.join(args)}")
    result = subprocess.run(
        ["ruff"] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace"  # Replace undecodable chars instead of crashing
    )

    stdout = result.stdout or ""
    stderr = result.stderr or ""

    print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(stdout)
        if stderr:
            f.write("\n" + stderr)

    _print_info(f"\nRuff report saved to: {report_path}")

    if result.returncode != 0 and suggest_fix:
        _print_warning(
            "Linting errors detected.\n"
            "Run `poetry run lint-fix` to apply fixes where possible.\n"
            "Run `poetry run lint-fix-rule <RULE_CODE>` to fix specific rules."
        )

    if result.returncode != 0:
        sys.exit(result.returncode)


def lint():
    """Run Ruff linter and log plain results"""
    _run_ruff(["check", "."], "ruff_report.log", suggest_fix=True)


def lint_fix():
    """Run Ruff with --fix to auto-correct issues"""
    _run_ruff(["check", ".", "--fix"], "ruff_fix_report.log")


def lint_fix_rule():
    """Run Ruff with --fix for specific rule(s) passed as arguments"""
    if len(sys.argv) < 2:
        _print_error(
            "Usage: poetry run lint-fix-rule <RULE_CODE> [RULE_CODE ...]"
        )
        sys.exit(1)

    rules = sys.argv[1:]
    args = ["check", ".", "--fix", "--fix-only"]
    for rule in rules:
        args += ["--select", rule]

    _run_ruff(args, "ruff_fix_rule_report.log")
