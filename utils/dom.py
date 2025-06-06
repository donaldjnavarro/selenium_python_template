from __future__ import annotations

import os
from pathlib import Path
import logging
logger = logging.getLogger(__name__)

def save_dom(driver, filename="page_dump.html"):
    """Save the current DOM from the Selenium driver to a local HTML file.

    Args:
        driver: The Selenium WebDriver instance.
        filename: The name of the file to save the DOM HTML content as.

    """
    dom = driver.execute_script("return document.documentElement.outerHTML;")
    file_path = Path(
        os.getenv("LATEST_REPORT_DIR", "unknown_dom")
    ) / "dom" / filename
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(dom)
    logger.info(f"DOM saved to {file_path}"
          " (This file will not be available in the timestamped archive)"
    )
