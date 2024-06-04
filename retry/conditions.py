import time
import random
from typing import Callable, Type, Optional, Any


# Stop conditions
def stop_after_attempt(attempts: int):
    """
    Stops retrying after a specified number of attempts.

    Args:
        attempts: The maximum number of attempts.
    """
    return lambda attempt, exception, result: attempt >= attempts


def stop_after_delay(seconds: int):
    """
    Stops retrying after a specified delay in seconds.

    Args:
        seconds: The maximum delay in seconds.
    """
    start_time = time.time()
    return lambda attempt, exception, result: (time.time() - start_time) >= seconds


def stop_before_delay(seconds: int):
    """
    Stops retrying just before a specified delay in seconds.

    Args:
        seconds: The delay in seconds before stopping.
    """
    start_time = time.time()
    return lambda attempt, exception, result: (time.time() - start_time) > seconds - 1


def combine_stop_conditions(*conditions: Callable[[int, Optional[Exception], Optional[Any]], bool]):
    """
    Combines multiple stop conditions using logical OR.

    Args:
        *conditions: The stop conditions to combine.
    """
    return lambda attempt, exception, result: any(cond(attempt, exception, result) for cond in conditions)


# Wait conditions
def wait_fixed(seconds: float):
    """
    Fixed wait time between retries.

    Args:
        seconds: The wait time in seconds.
    """
    return lambda attempt: seconds


def wait_random(min_seconds: float, max_seconds: float):
    """
    Random wait time between retries.

    Args:
        min_seconds: The minimum wait time in seconds.
        max_seconds: The maximum wait time in seconds.
    """
    return lambda attempt: random.uniform(min_seconds, max_seconds)


def wait_random_exponential(multiplier: float = 1, max_seconds: float = 60):
    """
    Random exponential backoff wait time between retries.

    Args:
        multiplier: The multiplier for the exponential backoff.
        max_seconds: The maximum wait time in seconds.
    """
    return lambda attempt: min(random.uniform(0, 2 ** (attempt - 1)) * multiplier, max_seconds)


def wait_chain(*delays: float):
    """
    Chain of fixed wait times between retries.

    Args:
        *delays: The wait times in seconds.
    """

    def wait_fn(attempt):
        if attempt - 1 < len(delays):
            return delays[attempt - 1]
        return delays[-1]

    return wait_fn


def wait_exponential(multiplier: int = 1, min_wait: int = 1, max_wait: int = 30):
    """
    Exponential backoff wait time between retries.

    Args:
        multiplier: The multiplier for the exponential backoff.
        min_wait: The minimum wait time in seconds.
        max_wait: The maximum wait time in seconds.
    """
    return lambda attempt: min(max(min_wait, multiplier * (2 ** (attempt - 1))), max_wait)


# Retry conditions
def retry_if_exception_type(exception_type: Type[Exception]):
    """
    Retries if the exception is of a specified type.

    Args:
        exception_type: The exception type that triggers a retry.
    """
    return lambda e: isinstance(e, exception_type)


def retry_if_not_exception_type(exception_type: Type[Exception]):
    """
    Retries if the exception is not of a specified type.

    Args:
        exception_type: The exception type that does not trigger a retry.
    """
    return lambda e: not isinstance(e, exception_type)


def retry_if_result(predicate: Callable[[Any], bool]):
    """
    Retries if the result satisfies a specified predicate.

    Args:
        predicate: The predicate to test the result.
    """
    return lambda result: predicate(result)


def retry_if_not_result(predicate: Callable[[Any], bool]):
    """
    Retries if the result does not satisfy a specified predicate.

    Args:
        predicate: The predicate to test the result.
    """
    return lambda result: not predicate(result)


def combine_retry_conditions(*conditions: Callable):
    """
    Combines multiple retry conditions using logical OR.

    Args:
        *conditions: The retry conditions to combine.
    """
    return lambda x: any(cond(x) for cond in conditions)
