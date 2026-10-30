"""
Structured logging pipeline configuration for SemanticShield AI.
"""

import logging
import sys


def setup_logging() -> logging.Logger:
    """
    Initializes structured application logger.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger("semanticshield_ai")


logger = setup_logging()
