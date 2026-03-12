"""
Centralized logging for the automation framework.

Purpose: Single logger used for execution tracing across driver, pages, and scripts.
Role: Writes to console and to a daily log file under reports/ for debugging and audits.
Architecture: Import 'logger' from this module; used by core, pages, scripts, conftest.
"""
import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logger(name: str = "myntra_automation", level: int = logging.INFO) -> logging.Logger:
    """Configure and return a logger with console and daily file output under reports/."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    log_dir = Path(__file__).parent.parent / "reports"
    log_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = log_dir / f"automation_{timestamp}.log"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()
