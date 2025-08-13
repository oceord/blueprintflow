import logging
from collections.abc import Callable, Generator
from contextlib import contextmanager
from functools import wraps
from typing import Any

logger = logging.getLogger()


@contextmanager
def log_context(name: str) -> Generator[None, None, None]:
    """Context manager for logging entry and exit points of a code block.

    This context manager logs an informational message when entering the context,
    logs any exceptions that occur within the context, and logs an informational
    message when exiting the context.

    Args:
        name (str): The name of the context to be logged.

    Yields:
        None: This context manager does not yield any values.

    Raises:
        Exception: Re-raises any exception that occurs within the context.
    """
    logger.info("Entering %s", name)
    try:
        yield
    except Exception:
        logger.exception("Exception in %s", name)
        raise
    finally:
        logger.info("Exiting %s", name)


def log_operation(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Decorator for logging function calls and their arguments.

    This decorator logs an informational message when the function is called,
    including the function name and its arguments. It uses the `log_context`
    context manager to log entry and exit points of the function call.

    Args:
        func (Callable[[Any], Any]): The function to be decorated.

    Returns:
        Callable[[Any], Any]: The wrapped function with logging.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        logger.info(
            "Calling %s with args: %s and kwargs: %s", func.__name__, args, kwargs
        )
        with log_context(func.__name__):
            result = func(*args, **kwargs)
        logger.info("%s returned %s", func.__name__, result)
        return result

    return wrapper
