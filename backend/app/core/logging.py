"""
Application-wide logging configuration.

Important: medical/session data must never be logged. Log identifiers
(user IDs, case IDs, request IDs) instead of raw patient content.
"""

import logging
import sys

from app.core.config import get_settings


def configure_logging() -> None:
    settings = get_settings()

    root = logging.getLogger()
    root.setLevel(settings.log_level.upper())

    # Avoid duplicate handlers on reload
    if root.handlers:
        return

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)

    # Keep noisy third-party loggers reasonable
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
