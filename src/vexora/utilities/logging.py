import logging
from functools import lru_cache
from typing import Any

from rich.logging import RichHandler

import vexora


def maybe_quote(value: Any) -> str:
    if isinstance(value, str):
        return f'"{value}"'
    return str(value)


@lru_cache
def get_logger(name: str | None = None) -> logging.Logger:
    """Retrieves a logger with the given name, or the root logger if no name is given.

    Args:
        name: The name of the logger to retrieve.

    Returns:
        The logger with the given name, or the root logger if no name is given.

    Example:
        Basic Usage of `get_logger`
        ```python
        from vexora.utilities.logging import get_logger

        logger = get_logger("vexora.test")
        logger.info("This is a test") # Output: vexora.test: This is a test

        debug_logger = get_logger("vexora.debug")
        debug_logger.debug_kv("TITLE", "log message", "green")
        ```

    """
    parent_logger = logging.getLogger("vexora")

    if name:
        # Append the name if given but allow explicit full names e.g. "vexora.test"
        # should not become "vexora.vexora.test"
        if not name.startswith(parent_logger.name + "."):
            logger = parent_logger.getChild(name)
        else:
            logger = logging.getLogger(name)
    else:
        logger = parent_logger

    return logger


def setup_logging(
    level: str | None = None,
) -> None:
    logger = get_logger()

    if level is not None:
        logger.setLevel(level)
    else:
        logger.setLevel(vexora.settings.log_level)

    logger.handlers.clear()

    handler = RichHandler(rich_tracebacks=True, markup=False)
    formatter = logging.Formatter("%(name)s: %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False
